import type {Task} from './types';
const request = async (path:string, init?:RequestInit) => { const c=new AbortController(); const t=setTimeout(()=>c.abort(),10000); try { const r=await fetch('/api'+path,{...init,signal:c.signal,headers:{'Content-Type':'application/json',...(init?.headers||{})}}); const data= r.status===204?null:await r.json(); if(!r.ok){const e:any=new Error(data?.code||'http');e.status=r.status;e.code=data?.code;throw e} return data; } finally {clearTimeout(t)} };
export const fetchTasks=()=>request('/tasks') as Promise<Task[]>;
export const createTask=(title:string)=>request('/tasks',{method:'POST',body:JSON.stringify({title})}) as Promise<Task>;
export const setCompleted=(id:number,completed:boolean)=>request(`/tasks/${id}`,{method:'PATCH',body:JSON.stringify({completed})}) as Promise<Task>;
export const deleteTask=(id:number)=>request(`/tasks/${id}`,{method:'DELETE'});
