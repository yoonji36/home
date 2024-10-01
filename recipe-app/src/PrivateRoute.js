import React from 'react';
import { Navigate } from 'react-router-dom';

// PrivateRoute 컴포넌트를 올바르게 내보내기 위해 default로 내보냄
const PrivateRoute = ({ component: Component, ...rest }) => {
    return (
      rest.isAuthenticated ? <Component {...rest} /> : <Navigate to="/login" />
    );
  };
  
  export default PrivateRoute;
