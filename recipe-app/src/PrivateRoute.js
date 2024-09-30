import { Navigate } from 'react-router-dom';

// PrivateRoute 컴포넌트를 올바르게 내보내기 위해 default로 내보냄
const PrivateRoute = ({ isAuthenticated, component: Component, ...rest }) => {
  return (
    isAuthenticated ? <Component {...rest} /> : <Navigate to="/login" />
  );
};

export default PrivateRoute;
