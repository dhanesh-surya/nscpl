# NSCPL PRIVATE LIMITED Website

A dynamic, production-ready website for NSCPL PRIVATE LIMITED built with Django and Bootstrap 5.

## Features

- **Sports & Event Management**: Manage sports events, tournaments, and activities
- **Team Management**: Handle teams and player profiles
- **News & Announcements**: Publish news and company updates
- **Media Gallery**: Upload and organize images/videos with categories and tags
- **Contact System**: Email-based contact form submissions
- **Responsive Design**: Bootstrap 5 with modern UI and AOS animations

## Technology Stack

- **Backend**: Django 5.x (Python 3.11+)
- **Frontend**: Bootstrap 5, AOS animations, Font Awesome icons
- **Database**: SQLite3 (development), PostgreSQL (production)
- **Styling**: Custom CSS with theme colors

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nscpl
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
nscpl_project/
├── core/           # Homepage, about, static pages
├── events/         # Sports events and tournaments
├── sports/         # Sports categories and activities
├── teams/          # Team and player management
├── news/           # News and announcements
├── gallery/        # Media library with categories
├── contact/        # Contact form handling
├── templates/      # HTML templates
├── static/         # CSS, JS, images
└── media/          # User uploaded files
```

## Configuration

### Development
- Uses SQLite3 database
- Debug mode enabled
- Console email backend

### Production
- Configure PostgreSQL database URL in `.env`
- Set `DEBUG=False`
- Configure email settings for contact form
- Set up static/media file serving

## Theme Colors

- **Primary**: #0A192F (Navy Blue)
- **Accent**: #00BFA6 (Teal)
- **Secondary**: #F5F5F5 (Light Gray)
- **Highlight**: #FF9800 (Sports Orange)

## Admin Panel

Access the Django admin panel at `/admin/` to manage:
- Events and tournaments
- Sports categories
- Teams and players
- News articles
- Gallery items
- Contact form submissions

## License

Private - NSCPL PRIVATE LIMITED
