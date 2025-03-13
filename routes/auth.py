from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import random
import string
from datetime import datetime, timedelta
from utils.excel_handler import save_user, get_user
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        otp = request.form.get('otp')
        
        if not email:
            flash('Email is required', 'error')
            return render_template('login.html')
        
        # First step: Send OTP
        if not otp:
            # In a real application, we would send an actual email
            # For demo purposes, we'll store it in session
            new_otp = generate_otp()
            session['otp'] = new_otp
            session['otp_email'] = email
            session['otp_expiry'] = (datetime.now() + timedelta(minutes=5)).timestamp()
            
            flash(f'OTP sent to your email (Demo OTP: {new_otp})', 'info')
            return render_template('login.html', email=email, show_otp=True)
        
        # Second step: Verify OTP
        stored_otp = session.get('otp')
        stored_email = session.get('otp_email')
        otp_expiry = session.get('otp_expiry')
        
        if not stored_otp or not stored_email or not otp_expiry:
            flash('OTP expired. Please try again', 'error')
            return render_template('login.html')
        
        if datetime.now().timestamp() > otp_expiry:
            flash('OTP expired. Please try again', 'error')
            return render_template('login.html')
        
        if email != stored_email or otp != stored_otp:
            flash('Invalid OTP', 'error')
            return render_template('login.html', email=email, show_otp=True)
        
        # OTP verified successfully
        user = get_user(email)
        if not user:
            flash('User not found. Please register first.', 'error')
            return redirect(url_for('auth.register'))
        
        session['user'] = user
        flash('Logged in successfully!', 'success')
        return redirect(url_for('appointments.dashboard'))
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        brief = request.form.get('brief', '')
        
        if not all([name, email, contact]):
            flash('Please fill in all required fields', 'error')
            return render_template('register.html')
        
        try:
            # Check if user already exists
            existing_user = get_user(email)
            if existing_user:
                flash('Email already registered', 'error')
                return render_template('register.html')
            
            # Save new user
            user_data = {
                'name': name,
                'email': email,
                'contact': contact,
                'brief': brief,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_user(user_data)
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))
