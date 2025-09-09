module.exports = {
  content: [
    "./pages/*.{html,js}",
    "./index.html",
    "./js/*.js",
    "./components/*.{html,js}"
  ],
  theme: {
    extend: {
      colors: {
        // Primary Colors - Deep Forest Green Theme
        primary: {
          50: "#F0F4ED", // light-forest-tint
          100: "#D9E5CC", // forest-tint-100
          200: "#B8CFA3", // forest-tint-200
          300: "#96B97A", // forest-tint-300
          400: "#75A351", // forest-tint-400
          500: "#548D28", // forest-tint-500
          600: "#2D5016", // deep-forest-green
          700: "#244012", // darker-forest
          800: "#1B300E", // darkest-forest
          900: "#12200A", // forest-black
          DEFAULT: "#2D5016", // deep-forest-green
        },
        
        // Secondary Colors - Fresh Leaf Green Theme
        secondary: {
          50: "#F2F7F4", // light-leaf-tint
          100: "#DDEAE1", // leaf-tint-100
          200: "#BBDDCC", // leaf-tint-200
          300: "#99D0B7", // leaf-tint-300
          400: "#77C3A2", // leaf-tint-400
          500: "#55B68D", // leaf-tint-500
          600: "#4A7C59", // fresh-leaf-green
          700: "#3E6347", // darker-leaf
          800: "#324A35", // darkest-leaf
          900: "#263123", // leaf-black
          DEFAULT: "#4A7C59", // fresh-leaf-green
        },
        
        // Accent Colors - Golden Harvest Yellow Theme
        accent: {
          50: "#FFFBF0", // light-harvest-tint
          100: "#FFF3CC", // harvest-tint-100
          200: "#FFE799", // harvest-tint-200
          300: "#FFDB66", // harvest-tint-300
          400: "#FFCF33", // harvest-tint-400
          500: "#FFC300", // harvest-tint-500
          600: "#FFB000", // golden-harvest-yellow
          700: "#CC8D00", // darker-harvest
          800: "#996A00", // darkest-harvest
          900: "#664700", // harvest-black
          DEFAULT: "#FFB000", // golden-harvest-yellow
        },
        
        // Background Colors
        background: "#FEFEFE", // coconut-white
        surface: {
          50: "#FFFFFF", // pure-white
          100: "#F8F9FA", // subtle-gray
          200: "#E9ECEF", // light-gray
          300: "#DEE2E6", // medium-gray
          400: "#CED4DA", // gray-400
          500: "#ADB5BD", // gray-500
          DEFAULT: "#F8F9FA", // subtle-gray
        },
        
        // Text Colors
        text: {
          primary: "#1A1A1A", // high-contrast-black
          secondary: "#6B7280", // clear-hierarchy-gray
          tertiary: "#9CA3AF", // light-text-gray
          inverse: "#FFFFFF", // white-text
        },
        
        // Status Colors - Success (Healthy Crop Green)
        success: {
          50: "#ECFDF5", // light-success-tint
          100: "#D1FAE5", // success-tint-100
          200: "#A7F3D0", // success-tint-200
          300: "#6EE7B7", // success-tint-300
          400: "#34D399", // success-tint-400
          500: "#10B981", // success-tint-500
          600: "#059669", // healthy-crop-green
          700: "#047857", // darker-success
          800: "#065F46", // darkest-success
          900: "#064E3B", // success-black
          DEFAULT: "#059669", // healthy-crop-green
        },
        
        // Warning Colors - Monsoon Amber
        warning: {
          50: "#FFFBEB", // light-warning-tint
          100: "#FEF3C7", // warning-tint-100
          200: "#FDE68A", // warning-tint-200
          300: "#FCD34D", // warning-tint-300
          400: "#FBBF24", // warning-tint-400
          500: "#F59E0B", // warning-tint-500
          600: "#D97706", // monsoon-amber
          700: "#B45309", // darker-warning
          800: "#92400E", // darkest-warning
          900: "#78350F", // warning-black
          DEFAULT: "#D97706", // monsoon-amber
        },
        
        // Error Colors - Urgent Red
        error: {
          50: "#FEF2F2", // light-error-tint
          100: "#FEE2E2", // error-tint-100
          200: "#FECACA", // error-tint-200
          300: "#FCA5A5", // error-tint-300
          400: "#F87171", // error-tint-400
          500: "#EF4444", // error-tint-500
          600: "#DC2626", // urgent-red
          700: "#B91C1C", // darker-error
          800: "#991B1B", // darkest-error
          900: "#7F1D1D", // error-black
          DEFAULT: "#DC2626", // urgent-red
        },
        
        // Border Colors
        border: {
          light: "#F3F4F6", // light-border-gray
          DEFAULT: "#E5E7EB", // subtle-border-gray
          dark: "#D1D5DB", // dark-border-gray
        },
      },
      
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        poppins: ['Poppins', 'sans-serif'],
        malayalam: ['Noto Sans Malayalam', 'sans-serif'],
      },
      
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
        '6xl': ['3.75rem', { lineHeight: '1' }],
      },
      
      boxShadow: {
        'chat': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'button': '0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      },
      
      animation: {
        'success': 'successPulse 600ms ease-in-out',
        'fade-in': 'fadeIn 300ms ease-in-out',
        'slide-up': 'slideUp 300ms ease-in-out',
      },
      
      keyframes: {
        successPulse: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.05)' },
          '100%': { transform: 'scale(1)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
      
      transitionDuration: {
        '200': '200ms',
        '300': '300ms',
      },
      
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
    },
  },
  plugins: [],
}