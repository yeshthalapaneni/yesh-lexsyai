# yesh-lexsyai ( A Legal Document Template Assistant )

## Overview

A web application that helps users fill legal document templates through an AI-powered conversational interface. Users upload DOCX files containing placeholders, engage in a chat-based Q&A to provide values, and download the completed document. The system extracts placeholders (in formats like `{{placeholder}}`, `[PLACEHOLDER]`, or `{placeholder}`), generates contextual questions using OpenAI's GPT-5 model, and fills the template with validated user responses.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Framework & Tooling**
- React 18 with TypeScript using Vite as the build tool
- Wouter for client-side routing (lightweight alternative to React Router)
- TanStack Query (React Query) for server state management and API caching
- Design system based on shadcn/ui components with Radix UI primitives

**UI Component Strategy**
- Comprehensive component library using Radix UI headless components
- Tailwind CSS with custom design tokens for consistent styling
- Custom theme system with CSS variables for light/dark mode support
- Design inspired by Linear's minimalism combined with document-centric applications

**State Management**
- Server state managed through React Query with custom query client configuration
- Session-based workflow tracking document upload, filling, and completion
- Real-time polling (3-second intervals) during document processing until completion
- Local state for UI interactions and form management

**Layout & Navigation**
- Single-page application with step-based workflow (Upload → Fill → Complete)
- Progress indicator showing current step (1/3, 2/3, 3/3)
- Responsive design with mobile-first approach using Tailwind breakpoints

### Backend Architecture

**Server Framework**
- Express.js server with TypeScript
- Custom Vite middleware integration for development HMR
- Session-based request logging with duration tracking
- Multer for multipart file upload handling (10MB limit)

**Document Processing Pipeline**
1. File upload and validation (DOCX only)
2. Text extraction using Mammoth.js
3. Placeholder detection via regex patterns (supports multiple formats)
4. Session creation and state management
5. Conversational AI interaction for data gathering
6. Template filling using Docxtemplater and PizZip
7. Document generation and download

**API Design**
- RESTful endpoints with Zod schema validation
- `/api/upload` - Document upload and analysis
- `/api/sessions/:id` - Session retrieval
- `/api/chat` - Conversational placeholder filling
- `/api/download/:id` - Completed document download
- Standardized error handling with descriptive messages

**Storage Strategy**
- In-memory storage implementation (MemStorage class)
- Extensible storage interface (IStorage) for future database integration
- Session management with UUID generation
- File buffer storage for uploaded documents
- Chat message history per session

### Data Storage Solutions

**Current Implementation**
- In-memory Map-based storage for sessions, messages, and file buffers
- No persistent database configured (ready for Drizzle ORM integration)

**Schema Design (Prepared for PostgreSQL)**
- `document_sessions` table with JSONB placeholder storage
- `chat_messages` table linked to sessions
- Drizzle ORM configuration ready with schema definitions
- Support for session states: uploading, analyzing, filling, completed

**Database Integration (Planned)**
- PostgreSQL via Neon Database (@neondatabase/serverless)
- Drizzle ORM for type-safe database queries
- Migration system configured (drizzle-kit)
- Connection pooling through Neon serverless driver

### Authentication and Authorization

**Current State**
- No authentication implemented
- Session-based workflow without user accounts
- Sessions identified by UUID only

**Security Considerations**
- File upload size limits (10MB)
- DOCX-only file type validation
- Input sanitization through Zod schemas
- Express JSON body size limits with raw body preservation

## External Dependencies

### AI Services
- **OpenAI GPT-5** - Conversational AI for generating contextual questions and validating user responses
- API key required via `OPENAI_API_KEY` environment variable
- Used for intelligent placeholder prompting and response processing

### Document Processing
- **Mammoth.js** - DOCX text extraction
- **Docxtemplater** - Template filling engine
- **PizZip** - ZIP file handling for DOCX manipulation

### Database (Configuration Ready)
- **Neon Database** - Serverless PostgreSQL hosting
- **Drizzle ORM** - Type-safe SQL query builder
- Connection string via `DATABASE_URL` environment variable

### UI Framework Components
- **Radix UI** - Comprehensive set of headless UI primitives (accordion, dialog, dropdown, select, tabs, toast, etc.)
- **shadcn/ui** - Pre-styled component patterns built on Radix UI
- **Tailwind CSS** - Utility-first CSS framework with custom configuration
- **Lucide React** - Icon library

### Development Tools
- **Vite** - Build tool and development server
- **TypeScript** - Type safety across frontend and backend
- **React Dropzone** - Drag-and-drop file upload interface
- **React Hook Form** with Zod resolvers for form validation
- **date-fns** - Date manipulation utilities

### Session Management
- **connect-pg-simple** - PostgreSQL session store (configured for future use)
- Custom session storage interface for flexibility
