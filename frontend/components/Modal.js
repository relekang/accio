import React from 'react';

import './Modal.styl';

export default function Modal({ children }) {
  return (
    <div className="Modal Modal--open">
      {children}
    </div>
  );
}
