import React from 'react';
import { get } from 'lodash';

import NotFound from '../containers/NotFound';

export default function havePropOr404(prop, Component) {
  const hoc = props => {
    if (get(props, prop)) {
      return <Component {...props} />;
    }
    return <NotFound {...props} />;
  };

  hoc.displayName = `PropOr404(${Component.displayName})`;
  return hoc;
}
