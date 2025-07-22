/**
 * Validation utilities for form inputs and data validation
 */

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export interface PasswordStrengthResult extends ValidationResult {
  strength: 'weak' | 'medium' | 'strong';
  score: number;
}

/**
 * Email validation using RFC 5322 compliant regex
 */
export const validateEmail = (email: string): ValidationResult => {
  const errors: string[] = [];
  
  if (!email.trim()) {
    errors.push('Email is required');
    return { isValid: false, errors };
  }
  
  // RFC 5322 compliant email regex (simplified)
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  
  if (!emailRegex.test(email)) {
    errors.push('Please enter a valid email address');
  }
  
  if (email.length > 254) {
    errors.push('Email address is too long');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

/**
 * Username validation
 */
export const validateUsername = (username: string): ValidationResult => {
  const errors: string[] = [];
  
  if (!username.trim()) {
    errors.push('Username is required');
    return { isValid: false, errors };
  }
  
  // Length validation
  if (username.length < 3) {
    errors.push('Username must be at least 3 characters long');
  }
  
  if (username.length > 20) {
    errors.push('Username must be no more than 20 characters long');
  }
  
  // Character validation
  if (!/^[a-zA-Z]/.test(username)) {
    errors.push('Username must start with a letter');
  }
  
  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    errors.push('Username can only contain letters, numbers, and underscores');
  }
  
  // Reserved usernames
  const reservedUsernames = ['admin', 'administrator', 'root', 'system', 'api', 'www'];
  if (reservedUsernames.includes(username.toLowerCase())) {
    errors.push('This username is not available');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

/**
 * Password strength validation
 */
export const validatePassword = (password: string): PasswordStrengthResult => {
  const errors: string[] = [];
  let score = 0;
  
  if (!password) {
    return {
      isValid: false,
      errors: ['Password is required'],
      strength: 'weak',
      score: 0
    };
  }
  
  // Length check
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  } else {
    score += 1;
    if (password.length >= 12) score += 1;
  }
  
  // Uppercase letter check
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  } else {
    score += 1;
  }
  
  // Lowercase letter check
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  } else {
    score += 1;
  }
  
  // Number check
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number');
  } else {
    score += 1;
  }
  
  // Special character check
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Password must contain at least one special character');
  } else {
    score += 1;
  }
  
  // Common patterns check
  const commonPatterns = [
    /(.)\1{2,}/, // Repeated characters (aaa, 111)
    /123|234|345|456|567|678|789|890/, // Sequential numbers
    /abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz/, // Sequential letters
    /password|12345|qwerty|letmein|welcome|admin|login/i // Common passwords
  ];
  
  commonPatterns.forEach(pattern => {
    if (pattern.test(password)) {
      errors.push('Password contains common patterns that are easy to guess');
      score = Math.max(0, score - 2);
    }
  });
  
  // Determine strength
  let strength: 'weak' | 'medium' | 'strong' = 'weak';
  if (score >= 5 && errors.length === 0) {
    strength = 'strong';
  } else if (score >= 3 && errors.length <= 1) {
    strength = 'medium';
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    strength,
    score
  };
};

/**
 * Phone number validation (international format)
 */
export const validatePhone = (phone: string): ValidationResult => {
  const errors: string[] = [];
  
  if (!phone.trim()) {
    // Phone is optional in most cases
    return { isValid: true, errors: [] };
  }
  
  // Remove all non-digit characters for validation
  const digitsOnly = phone.replace(/\D/g, '');
  
  // Check length (7-15 digits as per ITU-T E.164)
  if (digitsOnly.length < 7 || digitsOnly.length > 15) {
    errors.push('Phone number must be between 7 and 15 digits');
  }
  
  // Basic format validation (allows various international formats)
  const phoneRegex = /^[\+]?[1-9][\d\s\-\(\)]{6,20}$/;
  if (!phoneRegex.test(phone)) {
    errors.push('Please enter a valid phone number');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

/**
 * Generic required field validation
 */
export const validateRequired = (value: string, fieldName: string): ValidationResult => {
  const errors: string[] = [];
  
  if (!value || !value.trim()) {
    errors.push(`${fieldName} is required`);
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

/**
 * Validate confirm password matches original password
 */
export const validatePasswordConfirmation = (password: string, confirmPassword: string): ValidationResult => {
  const errors: string[] = [];
  
  if (!confirmPassword.trim()) {
    errors.push('Password confirmation is required');
  } else if (password !== confirmPassword) {
    errors.push('Passwords do not match');
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};

/**
 * Sanitize user input to prevent XSS
 */
export const sanitizeInput = (input: string): string => {
  if (!input) return '';
  
  return input
    .replace(/[<>]/g, '') // Remove potential HTML tags
    .trim();
};

/**
 * Validate multiple fields at once
 */
export const validateMultiple = (validators: Array<() => ValidationResult>): ValidationResult => {
  const allErrors: string[] = [];
  let isValid = true;
  
  validators.forEach(validator => {
    const result = validator();
    if (!result.isValid) {
      isValid = false;
      allErrors.push(...result.errors);
    }
  });
  
  return {
    isValid,
    errors: allErrors
  };
};

/**
 * Debounced validation function
 */
export const createDebouncedValidator = (
  validator: (value: string) => ValidationResult,
  delay: number = 300
) => {
  let timeoutId: number;
  
  return (value: string): Promise<ValidationResult> => {
    return new Promise((resolve) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        resolve(validator(value));
      }, delay);
    });
  };
};

/**
 * Get password strength color class for UI
 */
export const getPasswordStrengthColor = (strength: 'weak' | 'medium' | 'strong'): string => {
  switch (strength) {
    case 'weak':
      return 'text-danger';
    case 'medium':
      return 'text-warning';
    case 'strong':
      return 'text-success';
    default:
      return 'text-muted';
  }
};

/**
 * Get password strength percentage for progress bars
 */
export const getPasswordStrengthPercentage = (strength: 'weak' | 'medium' | 'strong'): number => {
  switch (strength) {
    case 'weak':
      return 25;
    case 'medium':
      return 60;
    case 'strong':
      return 100;
    default:
      return 0;
  }
};

/**
 * Form validation helpers
 */
export const formValidation = {
  email: validateEmail,
  username: validateUsername,
  password: validatePassword,
  phone: validatePhone,
  required: validateRequired,
  passwordConfirmation: validatePasswordConfirmation,
  sanitize: sanitizeInput,
  multiple: validateMultiple,
  debounced: createDebouncedValidator
};

export default formValidation; 