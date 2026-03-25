# AGENTS.md - Invitaciones Digitales API

## 1. Project Overview

**Project Name:** invitaciones_fastapi  
**Description:** Web application for digital invitations with event management, RSVP, and playlist features.  
**Type:** Full-stack web application (FastAPI + Vue 3)

## 2. Technology Stack

### Backend
- **Framework:** FastAPI
- **ORM:** SQLAlchemy (async)
- **Database:** MariaDB (via aiomysql)
- **Migrations:** Alembic
- **Image Processing:** Pillow
- **Runtime:** Python 3.11

### Frontend
- **Framework:** Vue 3 (Composition API)
- **Build Tool:** Vite
- **Router:** Vue Router 5
- **Icons:** Font Awesome 6

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **Ports:** Backend (8000), Frontend (8081), MariaDB (3306)

## 3. Project Structure

```
invitaciones_fastapi/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Settings from .env
│   │   ├── database.py          # SQLAlchemy async setup
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── crud.py              # Database operations
│   │   ├── image_utils.py       # Image processing (resize, WebP)
│   │   └── routers/
│   │       ├── invitaciones.py  # Public invitation endpoint
│   │       ├── clientes.py      # Client CRUD + image upload
│   │       └── templates.py     # Template CRUD
│   ├── uploads/                 # Uploaded images (auto-created)
│   ├── alembic/                 # Database migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api.js              # API client functions
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── router/index.js     # Vue Router config
│   │   ├── layouts/AdminLayout.vue
│   │   ├── views/
│   │   │   ├── InvitationView.vue
│   │   │   ├── Clientes.vue
│   │   │   ├── Templates.vue
│   │   │   └── Login.vue
│   │   ├── components/
│   │   │   ├── ClientForm.vue
│   │   │   ├── TemplateForm.vue
│   │   │   ├── RsvpForm.vue
│   │   │   ├── PlaylistForm.vue
│   │   │   └── ... (event, ceremony, gallery, etc.)
│   │   └── invitation-templates/
│   │       └── BaseTemplate.vue
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

## 4. API Endpoints

### Public Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/{event_type}/{slug}` | Get invitation by event type and slug |
| POST | `/clientes/{id}/confirmaciones/` | Submit RSVP confirmation |
| POST | `/clientes/{id}/canciones/` | Submit song request for playlist |

### Admin Endpoints (Clientes)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/clientes/` | List all clients |
| POST | `/clientes/` | Create client |
| GET | `/clientes/{id}` | Get client details |
| PUT | `/clientes/{id}` | Update client |
| DELETE | `/clientes/{id}` | Delete client |
| GET | `/clientes/slug/{slug}` | Get client by slug |
| POST | `/clientes/{id}/image` | Upload client image |

### Admin Endpoints (Templates)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/templates/` | List all templates |
| POST | `/templates/` | Create template |
| GET | `/templates/{id}` | Get template |
| PUT | `/templates/{id}` | Update template |
| DELETE | `/templates/{id}` | Delete template |

## 5. Data Models

### Template
- `id`, `nombre`, `slug`, `descripcion`, `preview`, `tipo_evento`

### Cliente
- Basic: `nombre`, `titulo`, `slug`, `email`, `telefono_envio_confirmacion`
- Event: `tipo_evento`, `fecha_evento`, `hora_evento`, `lugar_evento`, `direccion_evento`
- Ceremony (optional): `fecha_ceremonia`, `hora_ceremonia`, `lugar_ceremonia`, `direccion_ceremonia`
- Personalization: `fuente_nombre`, `mensaje_bienvenida`, `codigo_vestimenta`, `instagram_url`, `alias_regalos`
- Visibility flags: `mostrar_ceremonia`, `mostrar_galeria`, `mostrar_dresscode`, `mostrar_instagram`, `mostrar_playlist`, `mostrar_regalos`
- Images: `imagen_fondo`, `imagen_fondo_ig`, `imagen1` - `imagen9`
- Relations: `template`, `confirmaciones`, `canciones`

### ConfirmacionAsistencia
- `id`, `cliente_id`, `nombre_invitado`, `email`, `telefono`, `asistencia`, `cantidad_acompanantes`, `restricciones_alimentarias`

### CancionPlaylist
- `id`, `cliente_id`, `nombre_interprete`, `nombre_tema`

## 6. Enums

### TipoEventoChoices
- `15` (Quinceañera), `boda` (Wedding), `cumple` (Birthday), `infantil` (Kids), `otros` (Others)

### GoogleFontsChoices
- `great_vibes`, `dancing_script`, `allura`, `sacramento`, `parisienne`

## 7. Environment Variables

Create `backend/.env`:
```env
DATABASE_URL=mysql+aiomysql://user:password@host:3306/dbname
MARIADB_DATABASE=invitaciones
MARIADB_USER=invitaciones_user
MARIADB_PASSWORD=secure_password
MARIADB_ROOT_PASSWORD=root_password
```

## 8. Commands

### Development (without Docker)
```bash
# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up --build
```

## 9. Key Features

- **Event Types:** Supports quinceañeras, weddings, birthdays, kids parties
- **Ceremony Info:** Optional ceremony details display
- **RSVP System:** Guests can confirm attendance
- **Playlist Requests:** Guests can suggest songs
- **Image Gallery:** Up to 9 images per invitation
- **Image Processing:** Auto-resize and WebP conversion (max 800px)
- **Theme Customization:** Font selection, dress code, Instagram link
- **Gift Registry:** Alias for gift registry

## 10. Frontend Routes

| Path | Component | Auth |
|------|-----------|------|
| `/` | Home (placeholder) | No |
| `/:tipo_evento/:slug` | InvitationView | No |
| `/admin/login` | Login | No |
| `/admin/clientes` | Clientes | Yes |
| `/admin/templates` | Templates | Yes |
