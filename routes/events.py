from flask import Blueprint, render_template, session, flash, redirect, url_for
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
events_bp = Blueprint('events', __name__)

# For demo purposes, we'll use a static list of events
# In a production environment, this would typically come from a database
SAMPLE_EVENTS = [
    {
        'title': 'Monthly Team Meeting',
        'date': '2024-02-01',
        'time': '10:00',
        'type': 'online',
        'location': 'Google Meet',
        'link': 'https://meet.google.com/sample-link',
        'description': 'Monthly team sync-up and project updates'
    },
    {
        'title': 'Client Workshop',
        'date': '2024-02-15',
        'time': '14:00',
        'type': 'offline',
        'location': 'WebbyTouch Infotech Office',
        'link': None,
        'description': 'Workshop on new technology implementation'
    }
]

@events_bp.route('/events')
def list_events():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # Sort events by date
        current_date = datetime.now()
        upcoming_events = []
        past_events = []
        
        for event in SAMPLE_EVENTS:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            if event_date >= current_date:
                upcoming_events.append(event)
            else:
                past_events.append(event)
        
        # Sort events by date
        upcoming_events.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        past_events.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        
        return render_template('events.html',
                             upcoming_events=upcoming_events,
                             past_events=past_events)
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}")
        flash('Error loading events', 'error')
        return render_template('events.html',
                             upcoming_events=[],
                             past_events=[])

@events_bp.route('/events/<event_date>')
def event_details(event_date):
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # Find event by date
        event = next((e for e in SAMPLE_EVENTS if e['date'] == event_date), None)
        
        if event:
            return render_template('event_details.html', event=event)
        else:
            flash('Event not found', 'error')
            return redirect(url_for('events.list_events'))
            
    except Exception as e:
        logger.error(f"Error fetching event details: {str(e)}")
        flash('Error loading event details', 'error')
        return redirect(url_for('events.list_events'))
