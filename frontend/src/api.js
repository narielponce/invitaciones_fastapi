const API_BASE_URL = '/api';

export async function getInvitationByEventTypeAndSlug(eventType, slug) {
  const response = await fetch(`${API_BASE_URL}/${eventType}/${slug}`);
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Invitación no encontrada');
    }
    throw new Error('Error al obtener los datos de la invitación');
  }
  return await response.json();
}

// --- Funciones Públicas ---

// DEPRECATED: This function is no longer the primary method for fetching invitations.
export async function getClienteBySlug_deprecated(slug) {
  const response = await fetch(`${API_BASE_URL}/clientes/slug/${slug}`);
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Invitación no encontrada');
    }
    throw new Error('Error al obtener los datos de la invitación');
  }
  return await response.json();
}

export async function createClienteConfirmacion(clienteId, confirmacionData) {
  const response = await fetch(`${API_BASE_URL}/clientes/${clienteId}/confirmaciones/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(confirmacionData),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Error al enviar confirmación: ${errorData.detail || response.statusText}`);
  }
  return await response.json();
}

export async function createClienteCancion(clienteId, cancionData) {
  const response = await fetch(`${API_BASE_URL}/clientes/${clienteId}/canciones/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(cancionData),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Error al sugerir canción: ${errorData.detail || response.statusText}`);
  }
  return await response.json();
}

// --- Funciones para Clientes (Admin) ---

export async function getClientes() {
  const response = await fetch(`${API_BASE_URL}/clientes/`);
  if (!response.ok) throw new Error('Error al obtener los clientes');
  return await response.json();
}

export async function createCliente(clienteData) {
  const response = await fetch(`${API_BASE_URL}/clientes/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(clienteData),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al crear el cliente');
  }
  return await response.json();
}

export async function updateCliente(id, clienteData) {
  const response = await fetch(`${API_BASE_URL}/clientes/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(clienteData),
  });
  if (!response.ok) {
     const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al actualizar el cliente');
  }
  return await response.json();
}

export async function deleteCliente(id) {
  const response = await fetch(`${API_BASE_URL}/clientes/${id}`, { method: 'DELETE' });
  if (!response.ok) throw new Error('Error al borrar el cliente');
  return await response.json();
}

export async function uploadClienteImage(clienteId, fieldName, file) {
  const formData = new FormData();
  formData.append('file', file);
  const response = await fetch(`${API_BASE_URL}/clientes/${clienteId}/image?field_name=${fieldName}`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Error al subir la imagen: ${errorData.detail || response.statusText}`);
  }
  return await response.json();
}

// --- Funciones para Templates (Admin) ---

export async function getTemplates() {
  const response = await fetch(`${API_BASE_URL}/templates/`);
  if (!response.ok) throw new Error('Error al obtener los templates');
  return await response.json();
}

export async function createTemplate(templateData) {
  const response = await fetch(`${API_BASE_URL}/templates/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(templateData),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al crear el template');
  }
  return await response.json();
}

export async function updateTemplate(id, templateData) {
  const response = await fetch(`${API_BASE_URL}/templates/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(templateData),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Error al actualizar el template');
  }
  return await response.json();
}

export async function deleteTemplate(id) {
  const response = await fetch(`${API_BASE_URL}/templates/${id}`, { method: 'DELETE' });
  if (!response.ok) throw new Error('Error al borrar el template');
  return await response.json();
}
