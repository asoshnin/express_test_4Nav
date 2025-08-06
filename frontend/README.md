# AI Navigator Profiler - Frontend

A modern, responsive React frontend for the AI Navigator Profiler assessment tool.

## 🚀 Features

- **Modern UI/UX** - Clean, professional design with smooth animations
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **Real-time Progress** - Visual progress tracking during assessment
- **Interactive Questions** - Engaging question interface with clear choices
- **Downloadable Reports** - One-click report download in Markdown format
- **Contact Integration** - Optional email subscription for updates

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful, customizable icons
- **Axios** - HTTP client for API communication

## 📦 Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🔧 Development

### Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── common/           # Shared components
│   │   │   ├── Header.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   └── assessment/       # Assessment-specific components
│   │       ├── ProgressBar.jsx
│   │       ├── QuestionDisplay.jsx
│   │       └── ReportViewer.jsx
│   ├── pages/               # Page components
│   │   ├── LandingPage.jsx
│   │   ├── AssessmentPage.jsx
│   │   └── ReportPage.jsx
│   ├── services/            # API services
│   │   └── api.js
│   ├── App.jsx             # Main app component
│   ├── main.jsx            # React entry point
│   └── index.css           # Global styles
├── public/                 # Static assets
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔗 API Integration

The frontend connects to the Azure Functions backend via the `/api` proxy configured in `vite.config.js`. This automatically routes API calls to `http://localhost:7071` during development.

### API Endpoints Used:
- `POST /api/assessment` - Start assessment
- `GET /api/assessment/{sessionId}/question` - Get next question
- `POST /api/assessment/{sessionId}/answer` - Submit answer
- `GET /api/assessment/{sessionId}/report` - Generate report
- `GET /api/assessment/{sessionId}/report/download` - Download report
- `POST /api/assessment/{sessionId}/contact` - Submit contact info

## 🎨 Design System

### Colors
- **Primary**: Blue (`primary-600`) - Main brand color
- **Secondary**: Gray scale - Text and backgrounds
- **Success**: Green - Positive states
- **Warning**: Amber - Important notices
- **Error**: Red - Error states

### Components
- **Cards** - `.card` class for content containers
- **Buttons** - `.btn-primary` and `.btn-secondary` classes
- **Inputs** - `.input-field` class for form inputs
- **Loading** - Custom spinner component

### Animations
- **Fade In** - `.animate-fade-in` for smooth transitions
- **Slide Up** - `.animate-slide-up` for content reveals
- **Pulse** - `.animate-pulse-slow` for loading states

## 🚀 Local Development Setup

### Prerequisites
1. **Backend Running** - Ensure your Azure Functions backend is running on `http://localhost:7071`
2. **Node.js** - Version 16 or higher
3. **npm** - Package manager

### Quick Start
```bash
# Terminal 1: Start backend (from project root)
cd express_assessor_4Navigators
func start

# Terminal 2: Start frontend
cd frontend
npm install
npm run dev
```

### Testing the Complete Flow
1. Open `http://localhost:3000`
2. Click "Start Your Assessment"
3. Answer questions (40 total)
4. View your personalized report
5. Download the report
6. Optionally subscribe for updates

## 📱 Responsive Design

The frontend is fully responsive and optimized for:
- **Desktop** - Full feature set with side-by-side layouts
- **Tablet** - Adapted layouts with touch-friendly interactions
- **Mobile** - Stacked layouts with optimized touch targets

## 🔒 Security Features

- **Input Validation** - Client-side validation for all forms
- **Error Handling** - Graceful error states with user-friendly messages
- **Loading States** - Clear feedback during API calls
- **Session Management** - Secure session handling

## 🎯 Performance

- **Fast Loading** - Vite for rapid development and optimized builds
- **Lazy Loading** - Components load as needed
- **Optimized Assets** - Compressed images and minified code
- **Caching** - Browser caching for static assets

## 🚀 Production Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Azure Static Web Apps
1. Build the project: `npm run build`
2. Deploy the `dist` folder to Azure Static Web Apps
3. Configure environment variables for production API endpoints

## 📞 Support

For issues or questions:
1. Check the browser console for errors
2. Verify the backend is running on port 7071
3. Ensure all environment variables are configured
4. Test API endpoints directly with curl or Postman

---

**Ready for local testing and development!** 🎉 