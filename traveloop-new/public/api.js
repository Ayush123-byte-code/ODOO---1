// ================================
// Traveloop - API Service
// Handles all backend communication
// ================================

const API_BASE_URL = 'http://localhost:5000/api';

// Token management
function getToken() {
    return localStorage.getItem('traveloop_token');
}

function setToken(token) {
    localStorage.setItem('traveloop_token', token);
}

function removeToken() {
    localStorage.removeItem('traveloop_token');
}

// API Request Helper
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = getToken();
    
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        },
        ...options
    };
    
    if (options.body && typeof options.body === 'object') {
        config.body = JSON.stringify(options.body);
    }
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error(`API Error [${endpoint}]:`, error.message);
        throw error;
    }
}

// ============== AUTH API ==============

const AuthAPI = {
    async signup(name, email, password) {
        const data = await apiRequest('/auth/signup', {
            method: 'POST',
            body: { name, email, password }
        });
        if (data.token) {
            setToken(data.token);
        }
        return data;
    },
    
    async login(email, password) {
        const data = await apiRequest('/auth/login', {
            method: 'POST',
            body: { email, password }
        });
        if (data.token) {
            setToken(data.token);
        }
        return data;
    },
    
    async logout() {
        try {
            await apiRequest('/auth/logout', { method: 'POST' });
        } finally {
            removeToken();
        }
    },
    
    async getCurrentUser() {
        return await apiRequest('/auth/me');
    },
    
    isAuthenticated() {
        return !!getToken();
    }
};

// ============== USER API ==============

const UserAPI = {
    async updateProfile(profileData) {
        return await apiRequest('/users/profile', {
            method: 'PUT',
            body: profileData
        });
    },
    
    async changePassword(currentPassword, newPassword) {
        return await apiRequest('/users/password', {
            method: 'PUT',
            body: { current_password: currentPassword, new_password: newPassword }
        });
    }
};

// ============== TRIPS API ==============

const TripsAPI = {
    async getAll(status = 'all') {
        const query = status !== 'all' ? `?status=${status}` : '';
        return await apiRequest(`/trips${query}`);
    },
    
    async getById(tripId) {
        return await apiRequest(`/trips/${tripId}`);
    },
    
    async create(tripData) {
        return await apiRequest('/trips', {
            method: 'POST',
            body: tripData
        });
    },
    
    async update(tripId, tripData) {
        return await apiRequest(`/trips/${tripId}`, {
            method: 'PUT',
            body: tripData
        });
    },
    
    async delete(tripId) {
        return await apiRequest(`/trips/${tripId}`, {
            method: 'DELETE'
        });
    },
    
    async getShared(shareCode) {
        return await apiRequest(`/trips/shared/${shareCode}`);
    },
    
    async copy(tripId) {
        return await apiRequest(`/trips/${tripId}/copy`, {
            method: 'POST'
        });
    }
};

// ============== STOPS API ==============

const StopsAPI = {
    async getForTrip(tripId) {
        return await apiRequest(`/trips/${tripId}/stops`);
    },
    
    async create(tripId, stopData) {
        return await apiRequest(`/trips/${tripId}/stops`, {
            method: 'POST',
            body: stopData
        });
    },
    
    async update(stopId, stopData) {
        return await apiRequest(`/stops/${stopId}`, {
            method: 'PUT',
            body: stopData
        });
    },
    
    async delete(stopId) {
        return await apiRequest(`/stops/${stopId}`, {
            method: 'DELETE'
        });
    }
};

// ============== ACTIVITIES API ==============

const ActivitiesAPI = {
    async create(stopId, activityData) {
        return await apiRequest(`/stops/${stopId}/activities`, {
            method: 'POST',
            body: activityData
        });
    },
    
    async update(activityId, activityData) {
        return await apiRequest(`/activities/${activityId}`, {
            method: 'PUT',
            body: activityData
        });
    },
    
    async delete(activityId) {
        return await apiRequest(`/activities/${activityId}`, {
            method: 'DELETE'
        });
    }
};

// ============== BUDGET API ==============

const BudgetAPI = {
    async getForTrip(tripId) {
        return await apiRequest(`/trips/${tripId}/budget`);
    },
    
    async addItem(tripId, itemData) {
        return await apiRequest(`/trips/${tripId}/budget`, {
            method: 'POST',
            body: itemData
        });
    },
    
    async deleteItem(itemId) {
        return await apiRequest(`/budget/${itemId}`, {
            method: 'DELETE'
        });
    }
};

// ============== PACKING API ==============

const PackingAPI = {
    async getForTrip(tripId) {
        return await apiRequest(`/trips/${tripId}/packing`);
    },
    
    async addItem(tripId, itemData) {
        return await apiRequest(`/trips/${tripId}/packing`, {
            method: 'POST',
            body: itemData
        });
    },
    
    async updateItem(itemId, itemData) {
        return await apiRequest(`/packing/${itemId}`, {
            method: 'PUT',
            body: itemData
        });
    },
    
    async deleteItem(itemId) {
        return await apiRequest(`/packing/${itemId}`, {
            method: 'DELETE'
        });
    }
};

// ============== NOTES API ==============

const NotesAPI = {
    async getForTrip(tripId) {
        return await apiRequest(`/trips/${tripId}/notes`);
    },
    
    async create(tripId, noteData) {
        return await apiRequest(`/trips/${tripId}/notes`, {
            method: 'POST',
            body: noteData
        });
    },
    
    async update(noteId, noteData) {
        return await apiRequest(`/notes/${noteId}`, {
            method: 'PUT',
            body: noteData
        });
    },
    
    async delete(noteId) {
        return await apiRequest(`/notes/${noteId}`, {
            method: 'DELETE'
        });
    }
};

// ============== DESTINATIONS API ==============

const DestinationsAPI = {
    async getSaved() {
        return await apiRequest('/destinations/saved');
    },
    
    async save(destinationData) {
        return await apiRequest('/destinations/saved', {
            method: 'POST',
            body: destinationData
        });
    },
    
    async remove(destinationId) {
        return await apiRequest(`/destinations/saved/${destinationId}`, {
            method: 'DELETE'
        });
    },
    
    async searchCities(query = '', region = '') {
        const params = new URLSearchParams();
        if (query) params.append('q', query);
        if (region) params.append('region', region);
        return await apiRequest(`/search/cities?${params}`);
    },
    
    async searchActivities(category = '') {
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        return await apiRequest(`/search/activities?${params}`);
    }
};

// ============== ADMIN API ==============

const AdminAPI = {
    async getStats() {
        return await apiRequest('/admin/stats');
    },
    
    async getUsers() {
        return await apiRequest('/admin/users');
    },
    
    async deleteUser(userId) {
        return await apiRequest(`/admin/users/${userId}`, {
            method: 'DELETE'
        });
    }
};

// Export all APIs
window.API = {
    Auth: AuthAPI,
    User: UserAPI,
    Trips: TripsAPI,
    Stops: StopsAPI,
    Activities: ActivitiesAPI,
    Budget: BudgetAPI,
    Packing: PackingAPI,
    Notes: NotesAPI,
    Destinations: DestinationsAPI,
    Admin: AdminAPI
};
