"use client";

import React, { useState } from 'react';

interface Filters {
  startDate: string;
  endDate: string;
  channel: string;
  country: string;
  deviceType: string;
  status: string; // 'all', 'valid', 'invalid'
}

interface FilterComponentProps {
  onApplyFilters: (filters: Filters) => void;
  onResetFilters: () => void;
}

const initialFilters: Filters = {
  startDate: '',
  endDate: '',
  channel: '',
  country: '',
  deviceType: '',
  status: 'all',
};

export default function FilterComponent({ onApplyFilters, onResetFilters }: FilterComponentProps) {
  const [filters, setFilters] = useState<Filters>(initialFilters);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onApplyFilters(filters);
  };

  const handleReset = () => {
    setFilters(initialFilters);
    onResetFilters();
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 shadow rounded-lg space-y-4 mb-6">
      <h3 className="text-lg font-semibold">Filtros Avançados</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div>
          <label htmlFor="startDate" className="block text-sm font-medium text-gray-700">Data Início</label>
          <input 
            type="date" 
            name="startDate" 
            id="startDate" 
            value={filters.startDate} 
            onChange={handleChange} 
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="endDate" className="block text-sm font-medium text-gray-700">Data Fim</label>
          <input 
            type="date" 
            name="endDate" 
            id="endDate" 
            value={filters.endDate} 
            onChange={handleChange} 
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="channel" className="block text-sm font-medium text-gray-700">Canal</label>
          <input 
            type="text" 
            name="channel" 
            id="channel" 
            placeholder="Ex: Google Ads, Orgânico"
            value={filters.channel} 
            onChange={handleChange} 
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="country" className="block text-sm font-medium text-gray-700">País</label>
          <input 
            type="text" 
            name="country" 
            id="country" 
            placeholder="Ex: BR, US"
            value={filters.country} 
            onChange={handleChange} 
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          />
        </div>
        <div>
          <label htmlFor="deviceType" className="block text-sm font-medium text-gray-700">Tipo de Dispositivo</label>
          <select 
            name="deviceType" 
            id="deviceType" 
            value={filters.deviceType} 
            onChange={handleChange} 
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
            <option value="">Todos</option>
            <option value="desktop">Desktop</option>
            <option value="mobile">Mobile</option>
            <option value="tablet">Tablet</option>
          </select>
        </div>
        <div>
          <label htmlFor="status" className="block text-sm font-medium text-gray-700">Status do Clique</label>
          <select 
            name="status" 
            id="status" 
            value={filters.status} 
            onChange={handleChange} 
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
            <option value="all">Todos</option>
            <option value="valid">Válido</option>
            <option value="invalid">Inválido</option>
          </select>
        </div>
      </div>
      <div className="flex justify-end space-x-3">
        <button 
          type="button"
          onClick={handleReset}
          className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Limpar Filtros
        </button>
        <button 
          type="submit"
          className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Aplicar Filtros
        </button>
      </div>
    </form>
  );
}

