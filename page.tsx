"use client";

import React, { useEffect, useState, useRef, useCallback } from 'react';
import io, { Socket } from 'socket.io-client';
import axios from 'axios';
import FilterComponent from '@/components/FilterComponent'; // Import the FilterComponent

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:5000';

interface EventLog {
  id: number;
  ip_address: string;
  user_agent: string;
  timestamp: string;
  url_accessed: string;
  referer_url: string | null;
  country: string | null;
  city: string | null;
  channel: string | null;
  device_type: string | null;
  is_valid_click: boolean;
  invalid_reason: string | null;
}

interface Metrics {
  total_events: number;
  valid_clicks: number;
  invalid_clicks: number;
  unique_ips: number;
}

interface AppliedFilters {
  startDate: string;
  endDate: string;
  channel: string;
  country: string;
  deviceType: string;
  status: string;
}

const initialMetrics: Metrics = { total_events: 0, valid_clicks: 0, invalid_clicks: 0, unique_ips: 0 };

export default function DashboardPage() {
  const [events, setEvents] = useState<EventLog[]>([]);
  const [metrics, setMetrics] = useState<Metrics | null>(initialMetrics);
  const [isConnected, setIsConnected] = useState(false);
  const socketRef = useRef<Socket | null>(null);
  const [currentFilters, setCurrentFilters] = useState<AppliedFilters | null>(null);
  const [logsPagination, setLogsPagination] = useState({ currentPage: 1, totalPages: 1, perPage: 10, totalLogs: 0 });

  const buildQueryString = (filters: AppliedFilters | null, page?: number, perPage?: number) => {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.startDate) params.append('start_date', filters.startDate);
      if (filters.endDate) params.append('end_date', filters.endDate);
      if (filters.channel) params.append('channel', filters.channel);
      if (filters.country) params.append('country', filters.country);
      if (filters.deviceType) params.append('device_type', filters.deviceType);
      if (filters.status && filters.status !== 'all') params.append('status', filters.status);
    }
    if (page) params.append('page', page.toString());
    if (perPage) params.append('per_page', perPage.toString());
    return params.toString();
  };

  const fetchMetrics = useCallback(async (filters: AppliedFilters | null) => {
    const queryString = buildQueryString(filters);
    try {
      const response = await axios.get(`${API_URL}/metrics?${queryString}`);
      setMetrics(response.data);
    } catch (error) {
      console.error("Error fetching metrics:", error);
      setMetrics(initialMetrics);
    }
  }, []);

  const fetchLogs = useCallback(async (filters: AppliedFilters | null, page = 1) => {
    const queryString = buildQueryString(filters, page, logsPagination.perPage);
    try {
      const response = await axios.get(`${API_URL}/logs?${queryString}`);
      setEvents(response.data.logs || []);
      setLogsPagination({
        currentPage: response.data.current_page,
        totalPages: response.data.total_pages,
        perPage: response.data.per_page,
        totalLogs: response.data.total_logs
      });
    } catch (error) {
      console.error("Error fetching logs:", error);
      setEvents([]);
    }
  }, [logsPagination.perPage]);

  useEffect(() => {
    fetchMetrics(currentFilters);
    fetchLogs(currentFilters, logsPagination.currentPage);

    const socket = io(WS_URL, {
      path: "/socket.io",
      transports: ['websocket'],
      namespace: "/tracking"
    });
    socketRef.current = socket;

    socket.on('connect', () => {
      console.log('Connected to WebSocket server in /tracking namespace');
      setIsConnected(true);
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server');
      setIsConnected(false);
    });

    socket.on('new_event', (newEvent: EventLog) => {
      console.log('Received new_event:', newEvent);
      // Check if the new event matches current filters before adding to the live table
      // This is a simplified check; a more robust one would involve checking all filter criteria
      let matchesFilters = true;
      if (currentFilters) {
        if (currentFilters.status && currentFilters.status !== 'all') {
          if ((currentFilters.status === 'valid' && !newEvent.is_valid_click) || 
              (currentFilters.status === 'invalid' && newEvent.is_valid_click)) {
            matchesFilters = false;
          }
        }
        // Add more checks for other filters if desired for live updates
      }

      if (matchesFilters) {
        setEvents(prevEvents => [newEvent, ...prevEvents].slice(0, logsPagination.perPage)); // Keep only one page size for live view
      }
      // Always update metrics, or refetch if complex
      fetchMetrics(currentFilters); 
    });

    socket.on('connect_error', (error) => {
      console.error('WebSocket Connection Error:', error);
      setIsConnected(false);
    });

    return () => {
      if (socketRef.current) {
        console.log("Disconnecting WebSocket");
        socketRef.current.disconnect();
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentFilters, logsPagination.currentPage]); // fetchMetrics and fetchLogs are memoized

  const handleApplyFilters = (filters: AppliedFilters) => {
    setCurrentFilters(filters);
    setLogsPagination(prev => ({ ...prev, currentPage: 1})); // Reset to first page on new filters
  };

  const handleResetFilters = () => {
    setCurrentFilters(null);
    setLogsPagination(prev => ({ ...prev, currentPage: 1})); 
  };

  const handlePageChange = (newPage: number) => {
    setLogsPagination(prev => ({ ...prev, currentPage: newPage }));
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Visão Geral do Tráfego</h2>
      
      <FilterComponent onApplyFilters={handleApplyFilters} onResetFilters={handleResetFilters} />

      {/* Metrics Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-4 shadow rounded-lg">
          <h3 className="text-gray-500 text-sm">Total de Eventos</h3>
          <p className="text-3xl font-bold">{metrics?.total_events ?? '0'}</p>
        </div>
        <div className="bg-white p-4 shadow rounded-lg">
          <h3 className="text-gray-500 text-sm">Cliques Válidos</h3>
          <p className="text-3xl font-bold text-green-600">{metrics?.valid_clicks ?? '0'}</p>
        </div>
        <div className="bg-white p-4 shadow rounded-lg">
          <h3 className="text-gray-500 text-sm">Cliques Inválidos</h3>
          <p className="text-3xl font-bold text-red-600">{metrics?.invalid_clicks ?? '0'}</p>
        </div>
        <div className="bg-white p-4 shadow rounded-lg">
          <h3 className="text-gray-500 text-sm">IPs Únicos (Filtrado)</h3>
          <p className="text-3xl font-bold">{metrics?.unique_ips ?? '0'}</p>
        </div>
      </div>

      <div className="bg-white p-4 shadow rounded-lg">
        <h3 className="text-xl font-semibold mb-2">Status da Conexão WebSocket: 
          <span className={isConnected ? 'text-green-500' : 'text-red-500'}>
            {isConnected ? 'Conectado' : 'Desconectado'}
          </span>
        </h3>
      </div>

      {/* Real-time/Filtered Events Table */}
      <div className="bg-white p-4 shadow rounded-lg">
        <h3 className="text-xl font-semibold mb-4">Logs de Eventos</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Timestamp</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">IP</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">País</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">URL Acessada</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Razão (Inválido)</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {events.length > 0 ? events.map((event) => (
                <tr key={event.id + '-' + event.timestamp} className={!event.is_valid_click ? 'bg-red-50' : ''}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{new Date(event.timestamp).toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{event.ip_address}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{event.country}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 truncate max-w-xs" title={event.url_accessed}>{event.url_accessed}</td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${event.is_valid_click ? 'text-green-600' : 'text-red-600'}`}>
                    {event.is_valid_click ? 'Válido' : 'Inválido'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{event.invalid_reason}</td>
                </tr>
              )) : (
                <tr>
                  <td colSpan={6} className="px-6 py-4 text-center text-sm text-gray-500">Nenhum evento encontrado para os filtros aplicados.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {/* Pagination Controls */}
        {logsPagination.totalPages > 1 && (
          <div className="mt-4 flex justify-between items-center">
            <button 
              onClick={() => handlePageChange(logsPagination.currentPage - 1)} 
              disabled={logsPagination.currentPage <= 1}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
            >
              Anterior
            </button>
            <span className="text-sm text-gray-700">
              Página {logsPagination.currentPage} de {logsPagination.totalPages} (Total: {logsPagination.totalLogs} logs)
            </span>
            <button 
              onClick={() => handlePageChange(logsPagination.currentPage + 1)} 
              disabled={logsPagination.currentPage >= logsPagination.totalPages}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50"
            >
              Próxima
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

