import React from 'react';
import ReactDOM from 'react-dom';
import Poststack from './poststack';

// This method is only called once
ReactDOM.render(
  // Insert the likes component into the DOM
  <Poststack url="/api/v1/p/" />,
  document.getElementById('reactEntry'),
);
