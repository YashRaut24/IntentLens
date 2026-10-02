const errorHandler = (err, req, res, next) => {
  console.error(`[Error Middleware] ${err.name}: ${err.message}`);

  let statusCode = res.statusCode === 200 ? 500 : res.statusCode;
  let message = err.message || 'Internal Server Error';

  if (err.name === 'ValidationError') {
    statusCode = 400;
    message = Object.values(err.errors).map((val) => val.message).join(', ');
  }

  if (err.name === 'CastError') {
    statusCode = 400;
    message = 'Resource not found or invalid identifier format';
  }

  res.status(statusCode).json({
    success: false,
    error: message,
    statusCode,
  });
};

module.exports = errorHandler;
