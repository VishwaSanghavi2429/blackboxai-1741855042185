from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import datetime
from utils.excel_handler import save_appointment, get_user_appointments
import logging

logger = logging.getLogger(__name__)
appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    user = session['user']
    try:
        # Get user's appointments
        appointments = get_user_appointments(user['email'])
        
        # Sort appointments by date
        upcoming_appointments = sorted(
            [apt for apt in appointments if datetime.strptime(apt['date'], '%Y-%m-%d') >= datetime.now()],
            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d')
        )
        
        return render_template('dashboard.html',
                             user=user,
                             appointments=upcoming_appointments[:5])  # Show only next 5 appointments
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {str(e)}")
        flash('Error loading dashboard data', 'error')
        return render_template('dashboard.html', user=user, appointments=[])

@appointments_bp.route('/book', methods=['GET', 'POST'])
def book_appointment():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        try:
            # Get form data
            date = request.form.get('date')
            time = request.form.get('time')
            call_type = request.form.get('call_type')  # 'domestic' or 'overseas'
            meeting_type = request.form.get('meeting_type')  # 'online' or 'offline'
            meeting_link = request.form.get('meeting_link', '')
            notes = request.form.get('notes', '')
            
            # Validate required fields
            if not all([date, time, call_type, meeting_type]):
                flash('Please fill in all required fields', 'error')
                return render_template('appointment.html')
            
            # Validate meeting link for online meetings
            if meeting_type == 'online' and not meeting_link:
                flash('Meeting link is required for online meetings', 'error')
                return render_template('appointment.html')
            
            # Create appointment data
            appointment_data = {
                'user_email': session['user']['email'],
                'date': date,
                'time': time,
                'call_type': call_type,
                'meeting_type': meeting_type,
                'meeting_link': meeting_link if meeting_type == 'online' else '',
                'notes': notes,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save appointment
            save_appointment(appointment_data)
            
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('appointments.dashboard'))
            
        except Exception as e:
            logger.error(f"Error booking appointment: {str(e)}")
            flash('An error occurred while booking the appointment. Please try again.', 'error')
            return render_template('appointment.html')
    
    return render_template('appointment.html')

@appointments_bp.route('/appointments')
def list_appointments():
    if 'user' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        user = session['user']
        appointments = get_user_appointments(user['email'])
        
        # Sort appointments by date
        appointments = sorted(
            appointments,
            key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
            reverse=True
        )
        
        return render_template('appointments_list.html',
                             appointments=appointments)
    except Exception as e:
        logger.error(f"Error fetching appointments: {str(e)}")
        flash('Error loading appointments', 'error')
        return render_template('appointments_list.html', appointments=[])
