import React from 'react';
import * as ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import MainPage from './MainPage';
import reportWebVitals from './reportWebVitals';
import './index.css';
import WeaponTool from './WeaponTool';
import Campaigns from './Campaigns';
import MindMapModal from './MindMap/MindMap';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const router = createBrowserRouter([
  {
    path: "/",
    element: <MainPage/>
  },
  {
    path: "/weapon-tool",
    element: <WeaponTool />
  },
  {
    path: "/campaigns",
    element: <Campaigns/>
  },
  {
    path: "/mind-map",
    element: <MindMapModal />
  },
  {
    path: '*',
    element: <div>Not found</div>
  }
])

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
