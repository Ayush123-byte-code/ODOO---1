// ================================
// Traveloop - Main Application JavaScript
// ================================

// State Management
const state = {
    currentUser: null,
    isLoggedIn: false,
    trips: [],
    currentTrip: null,
    packingItems: [],
    notes: [],
    cities: [],
    activities: []
};

// Sample Data
const sampleCities = [
    { id: 1, name: 'Paris', country: 'France', region: 'europe', image: 'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=400&h=300&fit=crop', costIndex: '$$$', popularity: 'Very Popular' },
    { id: 2, name: 'Tokyo', country: 'Japan', region: 'asia', image: 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&h=300&fit=crop', costIndex: '$$$$', popularity: 'Very Popular' },
    { id: 3, name: 'New York', country: 'USA', region: 'americas', image: 'https://images.unsplash.com/photo-1518391846015-55a9cc003b25?w=400&h=300&fit=crop', costIndex: '$$$$', popularity: 'Very Popular' },
    { id: 4, name: 'Bali', country: 'Indonesia', region: 'asia', image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&h=300&fit=crop', costIndex: '$$', popularity: 'Popular' },
    { id: 5, name: 'Santorini', country: 'Greece', region: 'europe', image: 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=400&h=300&fit=crop', costIndex: '$$$', popularity: 'Popular' },
    { id: 6, name: 'Dubai', country: 'UAE', region: 'asia', image: 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&h=300&fit=crop', costIndex: '$$$$', popularity: 'Popular' },
    { id: 7, name: 'Barcelona', country: 'Spain', region: 'europe', image: 'https://images.unsplash.com/photo-1583422409516-2895a77efded?w=400&h=300&fit=crop', costIndex: '$$', popularity: 'Popular' },
    { id: 8, name: 'Sydney', country: 'Australia', region: 'oceania', image: 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=400&h=300&fit=crop', costIndex: '$$$', popularity: 'Popular' },
    { id: 9, name: 'Rome', country: 'Italy', region: 'europe', image: 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&h=300&fit=crop', costIndex: '$$', popularity: 'Very Popular' },
    { id: 10, name: 'Cape Town', country: 'South Africa', region: 'africa', image: 'https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=400&h=300&fit=crop', costIndex: '$$', popularity: 'Growing' },
    { id: 11, name: 'Machu Picchu', country: 'Peru', region: 'americas', image: 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=400&h=300&fit=crop', costIndex: '$$', popularity: 'Popular' },
    { id: 12, name: 'Maldives', country: 'Maldives', region: 'asia', image: 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=400&h=300&fit=crop', costIndex: '$$$$', popularity: 'Popular' }
];

const sampleActivities = [
    { id: 1, name: 'Eiffel Tower Visit', category: 'sightseeing', city: 'Paris', image: 'https://images.unsplash.com/photo-1511739001486-6bfe10ce65f4?w=400&h=300&fit=crop', duration: '3 hours', cost: 26 },
    { id: 2, name: 'Sushi Making Class', category: 'food', city: 'Tokyo', image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=400&h=300&fit=crop', duration: '4 hours', cost: 85 },
    { id: 3, name: 'Central Park Walking Tour', category: 'nature', city: 'New York', image: 'https://images.unsplash.com/photo-1534430480872-3498386e7856?w=400&h=300&fit=crop', duration: '2 hours', cost: 25 },
    { id: 4, name: 'Temple Visit & Meditation', category: 'culture', city: 'Bali', image: 'https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=400&h=300&fit=crop', duration: '3 hours', cost: 15 },
    { id: 5, name: 'Sunset Sailing', category: 'adventure', city: 'Santorini', image: 'https://images.unsplash.com/photo-1534423861386-85a16f5d13fd?w=400&h=300&fit=crop', duration: '4 hours', cost: 120 },
    { id: 6, name: 'Desert Safari', category: 'adventure', city: 'Dubai', image: 'https://images.unsplash.com/photo-1451337516015-6b6e9a44a8a3?w=400&h=300&fit=crop', duration: '6 hours', cost: 95 },
    { id: 7, name: 'Tapas Walking Tour', category: 'food', city: 'Barcelona', image: 'https://images.unsplash.com/photo-1515443961218-a51367888e4b?w=400&h=300&fit=crop', duration: '3 hours', cost: 75 },
    { id: 8, name: 'Opera House Tour', category: 'culture', city: 'Sydney', image: 'https://images.unsplash.com/photo-1523059623039-a9ed027e7fad?w=400&h=300&fit=crop', duration: '1.5 hours', cost: 40 },
    { id: 9, name: 'Colosseum Guided Tour', category: 'sightseeing', city: 'Rome', image: 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&h=300&fit=crop', duration: '3 hours', cost: 55 },
    { id: 10, name: 'Table Mountain Hike', category: 'nature', city: 'Cape Town', image: 'https://images.unsplash.com/photo-1576485375217-d6a95e34d043?w=400&h=300&fit=crop', duration: '5 hours', cost: 30 },
    { id: 11, name: 'Inca Trail Trek', category: 'adventure', city: 'Machu Picchu', image: 'https://images.unsplash.com/photo-1526392060635-9d6019884377?w=400&h=300&fit=crop', duration: '4 days', cost: 350 },
    { id: 12, name: 'Snorkeling Adventure', category: 'nature', city: 'Maldives', image: 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=400&h=300&fit=crop', duration: '3 hours', cost: 65 }
];

const defaultPackingItems = [
    { id: 1, name: 'Passport', category: 'documents', packed: false },
    { id: 2, name: 'Travel Insurance', category: 'documents', packed: false },
    { id: 3, name: 'Phone Charger', category: 'electronics', packed: false },
    { id: 4, name: 'Camera', category: 'electronics', packed: false },
    { id: 5, name: 'T-shirts', category: 'clothing', packed: false },
    { id: 6, name: 'Pants/Shorts', category: 'clothing', packed: false },
    { id: 7, name: 'Underwear', category: 'clothing', packed: false },
    { id: 8, name: 'Toothbrush', category: 'toiletries', packed: false },
    { id: 9, name: 'Sunscreen', category: 'toiletries', packed: false },
    { id: 10, name: 'Medications', category: 'toiletries', packed: false }
];

// Initialize
state.cities = sampleCities;
state.activities = sampleActivities;
state.packingItems = [...defaultPackingItems];

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    // Load state from localStorage
    loadState();
    
    // Initialize UI
    renderRecentTrips();
    renderCities();
    renderActivities();
    renderPackingList();
    renderNotes();
    
    // Setup event listeners
    setupEventListeners();
    
    // Check auth state
    updateAuthUI();
    
    // Initialize upload area
    setupUploadArea();
}

function setupEventListeners() {
    // Filter buttons for My Trips
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            filterTrips(e.target.dataset.filter);
        });
    });

    // Filter chips for cities
    document.querySelectorAll('.chip[data-region]').forEach(chip => {
        chip.addEventListener('click', (e) => {
            document.querySelectorAll('.chip[data-region]').forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');
            filterCities(e.target.dataset.region);
        });
    });

    // Filter chips for activities
    document.querySelectorAll('.chip[data-type]').forEach(chip => {
        chip.addEventListener('click', (e) => {
            document.querySelectorAll('.chip[data-type]').forEach(c => c.classList.remove('active'));
            e.target.classList.add('active');
            filterActivities(e.target.dataset.type);
        });
    });

    // View toggle for itinerary
    document.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            toggleItineraryView(e.target.dataset.view);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAllModals();
        }
    });
}

// Screen Navigation
function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show target screen
    const targetScreen = document.getElementById(`${screenId}-screen`);
    if (targetScreen) {
        targetScreen.classList.add('active');
    }
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.screen === screenId) {
            link.classList.add('active');
        }
    });
    
    // Special handling for certain screens
    if (screenId === 'my-trips') {
        renderTripsList();
    }
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Mobile Menu
function toggleMobileMenu() {
    const navLinks = document.getElementById('navLinks');
    navLinks.classList.toggle('active');
}

// Authentication
function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    // Simulate login
    if (email && password) {
        state.currentUser = {
            name: email.split('@')[0],
            email: email
        };
        state.isLoggedIn = true;
        saveState();
        updateAuthUI();
        showToast('Welcome back!', 'success');
        showScreen('home');
    }
}

function handleSignup(e) {
    e.preventDefault();
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showToast('Passwords do not match', 'error');
        return;
    }
    
    // Simulate signup
    state.currentUser = { name, email };
    state.isLoggedIn = true;
    saveState();
    updateAuthUI();
    showToast('Account created successfully!', 'success');
    showScreen('home');
}

function updateAuthUI() {
    const authBtn = document.getElementById('authBtn');
    if (state.isLoggedIn) {
        authBtn.textContent = 'Sign Out';
        authBtn.onclick = logout;
    } else {
        authBtn.textContent = 'Sign In';
        authBtn.onclick = () => showScreen('login');
    }
}

function logout() {
    state.currentUser = null;
    state.isLoggedIn = false;
    saveState();
    updateAuthUI();
    showToast('Signed out successfully', 'success');
    showScreen('home');
}

// Trip Management
function handleCreateTrip(e) {
    e.preventDefault();
    
    const name = document.getElementById('tripName').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const description = document.getElementById('tripDescription').value;
    
    const newTrip = {
        id: Date.now(),
        name,
        startDate,
        endDate,
        description,
        coverImage: 'https://images.unsplash.com/photo-1488085061387-422e29b40080?w=400&h=300&fit=crop',
        stops: [],
        activities: [],
        budget: {
            transport: 0,
            accommodation: 0,
            activities: 0,
            meals: 0
        },
        createdAt: new Date().toISOString()
    };
    
    state.trips.push(newTrip);
    state.currentTrip = newTrip;
    saveState();
    
    // Clear form
    e.target.reset();
    document.getElementById('coverPreview').classList.remove('visible');
    
    showToast('Trip created successfully!', 'success');
    renderRecentTrips();
    showScreen('itinerary-builder');
    renderStops();
}

function renderRecentTrips() {
    const grid = document.getElementById('recentTripsGrid');
    const emptyState = document.getElementById('noTripsState');
    
    if (state.trips.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    emptyState.style.display = 'none';
    
    const recentTrips = state.trips.slice(-3).reverse();
    grid.innerHTML = recentTrips.map(trip => createTripCard(trip)).join('');
}

function renderTripsList() {
    const list = document.getElementById('tripsList');
    const emptyState = document.getElementById('noTripsMyTrips');
    
    if (state.trips.length === 0) {
        list.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    list.style.display = 'grid';
    emptyState.style.display = 'none';
    
    list.innerHTML = state.trips.map(trip => createTripCard(trip, true)).join('');
}

function createTripCard(trip, showActions = false) {
    const startDate = new Date(trip.startDate);
    const endDate = new Date(trip.endDate);
    const dateRange = `${formatDate(startDate)} - ${formatDate(endDate)}`;
    
    return `
        <div class="trip-card" onclick="openTrip(${trip.id})">
            <div class="trip-image">
                <img src="${trip.coverImage}" alt="${trip.name}">
            </div>
            <div class="trip-info">
                <h3 class="trip-name">${trip.name}</h3>
                <div class="trip-dates">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                        <line x1="16" y1="2" x2="16" y2="6"/>
                        <line x1="8" y1="2" x2="8" y2="6"/>
                        <line x1="3" y1="10" x2="21" y2="10"/>
                    </svg>
                    ${dateRange}
                </div>
                <div class="trip-meta">
                    <span class="trip-stops">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                            <circle cx="12" cy="10" r="3"/>
                        </svg>
                        ${trip.stops.length} stops
                    </span>
                    ${showActions ? `
                        <div class="trip-actions">
                            <button onclick="event.stopPropagation(); editTrip(${trip.id})" title="Edit">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                                </svg>
                            </button>
                            <button onclick="event.stopPropagation(); shareTrip(${trip.id})" title="Share">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="18" cy="5" r="3"/>
                                    <circle cx="6" cy="12" r="3"/>
                                    <circle cx="18" cy="19" r="3"/>
                                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/>
                                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>
                                </svg>
                            </button>
                            <button onclick="event.stopPropagation(); deleteTrip(${trip.id})" title="Delete">
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <polyline points="3,6 5,6 21,6"/>
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                                </svg>
                            </button>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
}

function openTrip(tripId) {
    const trip = state.trips.find(t => t.id === tripId);
    if (trip) {
        state.currentTrip = trip;
        document.getElementById('builderTripName').textContent = trip.name;
        renderStops();
        showScreen('itinerary-builder');
    }
}

function editTrip(tripId) {
    openTrip(tripId);
}

function shareTrip(tripId) {
    const trip = state.trips.find(t => t.id === tripId);
    if (trip) {
        document.getElementById('sharedTripName').textContent = trip.name;
        document.getElementById('sharedDates').textContent = `${formatDate(new Date(trip.startDate))} - ${formatDate(new Date(trip.endDate))}`;
        document.getElementById('sharedBy').textContent = state.currentUser?.name || 'Anonymous';
        renderSharedItinerary(trip);
        showScreen('shared');
    }
}

function deleteTrip(tripId) {
    if (confirm('Are you sure you want to delete this trip?')) {
        state.trips = state.trips.filter(t => t.id !== tripId);
        saveState();
        renderRecentTrips();
        renderTripsList();
        showToast('Trip deleted', 'success');
    }
}

function filterTrips(filter) {
    const today = new Date();
    let filteredTrips = [...state.trips];
    
    if (filter === 'upcoming') {
        filteredTrips = state.trips.filter(t => new Date(t.startDate) > today);
    } else if (filter === 'past') {
        filteredTrips = state.trips.filter(t => new Date(t.endDate) < today);
    }
    
    const list = document.getElementById('tripsList');
    list.innerHTML = filteredTrips.map(trip => createTripCard(trip, true)).join('');
}

// Stops Management
function openAddStopModal() {
    document.getElementById('addStopModal').classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
}

function addStop(e) {
    e.preventDefault();
    
    const city = document.getElementById('stopCity').value;
    const arrival = document.getElementById('stopArrival').value;
    const departure = document.getElementById('stopDeparture').value;
    
    const stop = {
        id: Date.now(),
        city,
        arrival,
        departure,
        activities: []
    };
    
    if (state.currentTrip) {
        state.currentTrip.stops.push(stop);
        saveState();
        renderStops();
        closeModal('addStopModal');
        e.target.reset();
        showToast('Stop added!', 'success');
    }
}

function renderStops() {
    const list = document.getElementById('stopsList');
    
    if (!state.currentTrip || state.currentTrip.stops.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                    <circle cx="12" cy="10" r="3"/>
                </svg>
                <h3>No stops yet</h3>
                <p>Add your first destination to start building your itinerary</p>
            </div>
        `;
        return;
    }
    
    list.innerHTML = state.currentTrip.stops.map(stop => `
        <div class="stop-card" draggable="true" data-stop-id="${stop.id}">
            <div class="stop-header">
                <div class="stop-info">
                    <h3>${stop.city}</h3>
                    <p>${formatDate(new Date(stop.arrival))} - ${formatDate(new Date(stop.departure))}</p>
                </div>
                <div class="stop-actions">
                    <button class="btn-icon" onclick="addActivityToStop(${stop.id})" title="Add Activity">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="12" y1="5" x2="12" y2="19"/>
                            <line x1="5" y1="12" x2="19" y2="12"/>
                        </svg>
                    </button>
                    <button class="btn-icon" onclick="removeStop(${stop.id})" title="Remove">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <line x1="18" y1="6" x2="6" y2="18"/>
                            <line x1="6" y1="6" x2="18" y2="18"/>
                        </svg>
                    </button>
                </div>
            </div>
            ${stop.activities.length > 0 ? `
                <div class="stop-activities">
                    ${stop.activities.map(a => `<span class="activity-tag">${a.name}</span>`).join('')}
                </div>
            ` : ''}
        </div>
    `).join('');
}

function removeStop(stopId) {
    if (state.currentTrip) {
        state.currentTrip.stops = state.currentTrip.stops.filter(s => s.id !== stopId);
        saveState();
        renderStops();
        showToast('Stop removed', 'success');
    }
}

function addActivityToStop(stopId) {
    // For now, show activities screen
    showScreen('activities');
}

// Itinerary View
function renderItineraryView() {
    const timeline = document.getElementById('itineraryTimeline');
    
    if (!state.currentTrip || state.currentTrip.stops.length === 0) {
        timeline.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                </svg>
                <h3>No itinerary yet</h3>
                <p>Add stops to your trip to see the timeline</p>
            </div>
        `;
        return;
    }
    
    timeline.innerHTML = state.currentTrip.stops.map((stop, index) => `
        <div class="timeline-day">
            <div class="timeline-dot"></div>
            <div class="timeline-header">
                <div class="timeline-date">Day ${index + 1}</div>
                <div class="timeline-city">${stop.city}</div>
            </div>
            <div class="timeline-activities">
                ${stop.activities.length > 0 ? stop.activities.map(activity => `
                    <div class="timeline-activity">
                        <span class="activity-time">${activity.time || '09:00'}</span>
                        <div class="activity-content">
                            <h4>${activity.name}</h4>
                            <p>${activity.description || 'No description'}</p>
                        </div>
                        <span class="activity-cost">$${activity.cost || 0}</span>
                    </div>
                `).join('') : `
                    <div class="timeline-activity">
                        <span class="activity-time">-</span>
                        <div class="activity-content">
                            <h4>Explore ${stop.city}</h4>
                            <p>Free time to discover the city</p>
                        </div>
                        <span class="activity-cost">$0</span>
                    </div>
                `}
            </div>
        </div>
    `).join('');
}

function toggleItineraryView(view) {
    // Toggle between timeline and list view
    console.log('Switching to view:', view);
}

// Cities
function renderCities(cities = state.cities) {
    const grid = document.getElementById('citiesGrid');
    grid.innerHTML = cities.map(city => `
        <div class="city-card">
            <div class="city-image">
                <img src="${city.image}" alt="${city.name}">
            </div>
            <div class="city-details">
                <h3>${city.name}</h3>
                <p class="country">${city.country}</p>
                <div class="city-meta">
                    <span class="popularity">${city.popularity}</span>
                    <button class="btn-add-city" onclick="addCityToTrip('${city.name}')">Add to Trip</button>
                </div>
            </div>
        </div>
    `).join('');
}

function handleCitySearch(query) {
    const filtered = state.cities.filter(city => 
        city.name.toLowerCase().includes(query.toLowerCase()) ||
        city.country.toLowerCase().includes(query.toLowerCase())
    );
    renderCities(filtered);
}

function filterCities(region) {
    if (region === 'all') {
        renderCities();
    } else {
        const filtered = state.cities.filter(city => city.region === region);
        renderCities(filtered);
    }
}

function addCityToTrip(cityName) {
    if (!state.currentTrip) {
        showToast('Please create or select a trip first', 'error');
        return;
    }
    
    // Open add stop modal with city pre-filled
    document.getElementById('stopCity').value = cityName;
    openAddStopModal();
}

// Activities
function renderActivities(activities = state.activities) {
    const grid = document.getElementById('activitiesGrid');
    grid.innerHTML = activities.map(activity => `
        <div class="activity-card">
            <div class="activity-image">
                <img src="${activity.image}" alt="${activity.name}">
            </div>
            <div class="activity-details">
                <h3>${activity.name}</h3>
                <p class="category">${activity.category} • ${activity.city}</p>
                <div class="activity-meta">
                    <span class="duration">${activity.duration} • $${activity.cost}</span>
                    <button class="btn-add-activity" onclick="addActivityToCurrentStop(${activity.id})">Add</button>
                </div>
            </div>
        </div>
    `).join('');
}

function handleActivitySearch(query) {
    const filtered = state.activities.filter(activity => 
        activity.name.toLowerCase().includes(query.toLowerCase()) ||
        activity.city.toLowerCase().includes(query.toLowerCase())
    );
    renderActivities(filtered);
}

function filterActivities(type) {
    if (type === 'all') {
        renderActivities();
    } else {
        const filtered = state.activities.filter(activity => activity.category === type);
        renderActivities(filtered);
    }
}

function addActivityToCurrentStop(activityId) {
    if (!state.currentTrip || state.currentTrip.stops.length === 0) {
        showToast('Please add a stop to your trip first', 'error');
        return;
    }
    
    const activity = state.activities.find(a => a.id === activityId);
    if (activity) {
        // Add to the last stop for simplicity
        const lastStop = state.currentTrip.stops[state.currentTrip.stops.length - 1];
        lastStop.activities.push(activity);
        saveState();
        showToast('Activity added!', 'success');
    }
}

// Packing List
function renderPackingList() {
    const container = document.getElementById('packingCategories');
    const categories = ['clothing', 'documents', 'electronics', 'toiletries', 'other'];
    
    container.innerHTML = categories.map(category => {
        const items = state.packingItems.filter(item => item.category === category);
        if (items.length === 0) return '';
        
        const packedCount = items.filter(item => item.packed).length;
        
        return `
            <div class="packing-category">
                <div class="category-header">
                    <h4>${category}</h4>
                    <span>${packedCount}/${items.length}</span>
                </div>
                <div class="packing-items">
                    ${items.map(item => `
                        <div class="packing-item ${item.packed ? 'checked' : ''}">
                            <input type="checkbox" id="pack-${item.id}" ${item.packed ? 'checked' : ''} onchange="togglePackItem(${item.id})">
                            <label for="pack-${item.id}">${item.name}</label>
                            <button class="btn-remove" onclick="removePackItem(${item.id})">&times;</button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }).join('');
    
    updatePackingProgress();
}

function addPackingItem() {
    const input = document.getElementById('newPackItem');
    const category = document.getElementById('packCategory').value;
    const name = input.value.trim();
    
    if (!name) return;
    
    state.packingItems.push({
        id: Date.now(),
        name,
        category,
        packed: false
    });
    
    input.value = '';
    saveState();
    renderPackingList();
    showToast('Item added!', 'success');
}

function togglePackItem(itemId) {
    const item = state.packingItems.find(i => i.id === itemId);
    if (item) {
        item.packed = !item.packed;
        saveState();
        renderPackingList();
    }
}

function removePackItem(itemId) {
    state.packingItems = state.packingItems.filter(i => i.id !== itemId);
    saveState();
    renderPackingList();
}

function updatePackingProgress() {
    const total = state.packingItems.length;
    const packed = state.packingItems.filter(i => i.packed).length;
    const percent = total > 0 ? (packed / total) * 100 : 0;
    
    document.getElementById('packingProgress').style.width = `${percent}%`;
    document.getElementById('packingProgressText').textContent = `${packed} of ${total} items packed`;
}

function resetPackingList() {
    state.packingItems = state.packingItems.map(item => ({...item, packed: false}));
    saveState();
    renderPackingList();
    showToast('Checklist reset', 'success');
}

// Notes
function renderNotes() {
    const list = document.getElementById('notesList');
    const emptyState = document.getElementById('noNotesState');
    
    if (state.notes.length === 0) {
        list.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    list.innerHTML = state.notes.map(note => `
        <div class="note-card">
            <div class="note-header">
                <span class="note-title">${note.title}</span>
                <span class="note-timestamp">${formatDateTime(new Date(note.createdAt))}</span>
            </div>
            <p class="note-content">${note.content}</p>
            ${note.stopId ? `<div class="note-stop">Linked to: Stop</div>` : ''}
        </div>
    `).join('');
}

function addNote() {
    document.getElementById('addNoteModal').classList.add('active');
}

function saveNote(e) {
    e.preventDefault();
    
    const title = document.getElementById('noteTitle').value;
    const content = document.getElementById('noteContent').value;
    const stopId = document.getElementById('noteStop').value;
    
    state.notes.push({
        id: Date.now(),
        title,
        content,
        stopId: stopId || null,
        createdAt: new Date().toISOString()
    });
    
    saveState();
    renderNotes();
    closeModal('addNoteModal');
    e.target.reset();
    showToast('Note saved!', 'success');
}

// Shared Itinerary
function renderSharedItinerary(trip) {
    const container = document.getElementById('sharedItinerary');
    
    if (trip.stops.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>This trip has no stops yet.</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div class="itinerary-timeline">
            ${trip.stops.map((stop, index) => `
                <div class="timeline-day">
                    <div class="timeline-dot"></div>
                    <div class="timeline-header">
                        <div class="timeline-date">Day ${index + 1}</div>
                        <div class="timeline-city">${stop.city}</div>
                    </div>
                    <div class="timeline-activities">
                        ${stop.activities.length > 0 ? stop.activities.map(activity => `
                            <div class="timeline-activity">
                                <span class="activity-time">${activity.time || '09:00'}</span>
                                <div class="activity-content">
                                    <h4>${activity.name}</h4>
                                    <p>${activity.description || ''}</p>
                                </div>
                                <span class="activity-cost">$${activity.cost || 0}</span>
                            </div>
                        `).join('') : `
                            <div class="timeline-activity">
                                <span class="activity-time">-</span>
                                <div class="activity-content">
                                    <h4>Explore ${stop.city}</h4>
                                    <p>Free time to discover the city</p>
                                </div>
                            </div>
                        `}
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

function copyTrip() {
    showToast('Trip copied to your account!', 'success');
}

function shareToSocial() {
    if (navigator.share) {
        navigator.share({
            title: 'Check out my trip on Traveloop!',
            url: window.location.href
        });
    } else {
        navigator.clipboard.writeText(window.location.href);
        showToast('Link copied to clipboard!', 'success');
    }
}

// Profile
function saveProfile(e) {
    e.preventDefault();
    
    if (state.currentUser) {
        state.currentUser.name = document.getElementById('profileName').value;
        state.currentUser.email = document.getElementById('profileEmail').value;
        saveState();
        showToast('Profile updated!', 'success');
    }
}

function confirmDeleteAccount() {
    if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        state.currentUser = null;
        state.isLoggedIn = false;
        state.trips = [];
        state.notes = [];
        saveState();
        showToast('Account deleted', 'success');
        showScreen('home');
        updateAuthUI();
    }
}

// Upload Area
function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('coverPhoto');
    const preview = document.getElementById('coverPreview');
    
    if (!uploadArea) return;
    
    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--accent-primary)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = 'var(--border-color)';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = 'var(--border-color)';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageUpload(file);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImageUpload(file);
        }
    });
}

function handleImageUpload(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('coverPreview');
        preview.src = e.target.result;
        preview.classList.add('visible');
    };
    reader.readAsDataURL(file);
}

// Utilities
function formatDate(date) {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function formatDateTime(date) {
    return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const messageEl = toast.querySelector('.toast-message');
    
    messageEl.textContent = message;
    toast.className = `toast active ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 3000);
}

// State Persistence
function saveState() {
    const dataToSave = {
        currentUser: state.currentUser,
        isLoggedIn: state.isLoggedIn,
        trips: state.trips,
        packingItems: state.packingItems,
        notes: state.notes
    };
    localStorage.setItem('traveloop_state', JSON.stringify(dataToSave));
}

function loadState() {
    const saved = localStorage.getItem('traveloop_state');
    if (saved) {
        const data = JSON.parse(saved);
        state.currentUser = data.currentUser;
        state.isLoggedIn = data.isLoggedIn;
        state.trips = data.trips || [];
        state.packingItems = data.packingItems || defaultPackingItems;
        state.notes = data.notes || [];
    }
}

// City Details View
function viewCityDetails(cityId) {
    // For now, just show the city search with that city highlighted
    showScreen('city-search');
}
