import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://locahost:8000/api/v1/ws';

export const api = axios.create({
    baseURL: API_URL,
    timeout: 10000,
});

export const ws = new WebSocket(WS_URL)