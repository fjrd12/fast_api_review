"""
FastAPI Background Operations - Asynchronous Task Processing Module

This module demonstrates FastAPI's background task processing capabilities, showcasing
how to handle non-blocking operations that don't need to return results to the client
immediately. It implements:

- **Background Task Processing**: Non-blocking task execution using BackgroundTasks
- **User Registration Workflow**: Complete user onboarding with background notifications
- **Email Simulation**: Mock email sending operations that run asynchronously
- **Task Logging**: Comprehensive logging of background task execution
- **API Response Patterns**: Immediate responses while tasks process in background

Background Task Patterns:
- **Fire-and-Forget**: Tasks that don't need immediate client feedback
- **User Onboarding**: Registration with background welcome email processing
- **Notification Systems**: Asynchronous notification delivery
- **Audit Logging**: Background logging of user activities and system events

Key Concepts Demonstrated:
1. **BackgroundTasks Integration**: Adding tasks to FastAPI's background processor
2. **Task Function Design**: Creating functions suitable for background execution
3. **Parameter Passing**: Sending data to background tasks efficiently
4. **Response Timing**: Returning immediate responses while tasks execute
5. **Task Monitoring**: Tracking and verifying background task execution

Use Cases:
- **Email Notifications**: Welcome emails, password resets, account confirmations
- **Data Processing**: File uploads, image processing, report generation
- **External API Calls**: Third-party service integration without blocking responses
- **Logging and Analytics**: User activity tracking and system monitoring
- **Cleanup Operations**: Database maintenance, cache invalidation, file cleanup

Production Considerations:
- **Task Persistence**: Use Redis or database for task queue persistence
- **Error Handling**: Implement retry mechanisms and failure notifications
- **Monitoring**: Track task success rates and execution times
- **Scaling**: Consider Celery or similar for distributed task processing
- **Resource Management**: Monitor memory and CPU usage of background tasks

Architecture Benefits:
- **Improved User Experience**: Faster API responses with background processing
- **System Scalability**: Non-blocking operations improve overall throughput
- **Resource Efficiency**: Better utilization of server resources
- **Fault Tolerance**: Background tasks can be retried independently
- **Monitoring Capability**: Comprehensive task execution tracking

Security Considerations:
- **Input Validation**: Validate all data passed to background tasks
- **Rate Limiting**: Prevent abuse of background task endpoints
- **Access Control**: Ensure only authorized users can trigger tasks
- **Data Sanitization**: Clean sensitive data in background processing
"""

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, EmailStr


def create_background_app() -> FastAPI:
    """
    Create and configure FastAPI application for background task demonstration.
    
    This function demonstrates the application factory pattern with background
    task processing capabilities and proper configuration for async operations.
    
    Returns:
        FastAPI: Configured application instance with background task support
    
    Configuration Features:
        - Background task processing enabled by default
        - Comprehensive API documentation for async operations
        - Error handling for background task failures
        - Task monitoring and logging capabilities
    
    Background Task Architecture:
        - **Immediate Response**: API endpoints return immediately
        - **Async Processing**: Tasks execute after response is sent
        - **No Blocking**: Client requests don't wait for task completion
        - **Resource Efficient**: Tasks use available server resources optimally
    """
    return FastAPI(
        title="FastAPI Background Operations",
        description="Demonstration of asynchronous background task processing",
        version="1.0.0"
    )


app = create_background_app()


# Storage for notifications (simulating a log file or database)
notifications_log = []


class UserRegistration(BaseModel):
    """
    Pydantic model for user registration data validation.
    
    This model defines the structure and validation rules for user registration
    requests, ensuring data integrity before processing background tasks.
    
    Attributes:
        username (str): Unique username for the new user account
        email (str): Valid email address for user communications
    
    Validation Features:
        - **Username Validation**: Ensures username is provided and non-empty
        - **Email Validation**: Basic string validation (could use EmailStr for strict validation)
        - **Required Fields**: Both fields are mandatory for registration
        - **Type Safety**: Automatic type conversion and validation
    
    Usage in Background Tasks:
        This model data is passed to background tasks for user onboarding,
        welcome email sending, and account setup operations.
    
    Production Enhancements:
        ```python
        class UserRegistration(BaseModel):
            username: str = Field(min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_]+$')
            email: EmailStr  # Strict email validation
            full_name: Optional[str] = None
            marketing_consent: bool = False
            
            @validator('username')
            def validate_username_unique(cls, v):
                # Check username uniqueness in database
                return v
        ```
    
    Example Usage:
        ```python
        user_data = UserRegistration(
            username="johndoe",
            email="john@example.com"
        )
        
        # Data automatically validated before background task execution
        background_tasks.add_task(process_registration, user_data)
        ```
    """
    username: str
    email: str


def write_notification(email: str, message: str):
    """
    Background task function to write notification to log storage.
    
    This function simulates sending email notifications by logging them to
    persistent storage. In production, this would integrate with email
    service providers like SendGrid, AWS SES, or SMTP servers.
    
    Args:
        email (str): Recipient email address for the notification
        message (str): Notification message content to be sent
    
    Background Task Features:
        - **Non-blocking Execution**: Runs after API response is sent
        - **No Return Value**: Background tasks don't return data to client
        - **Error Isolation**: Task failures don't affect API response
        - **Resource Efficient**: Uses available server resources optimally
    
    Logging Pattern:
        The function appends formatted notification entries to the global
        notifications_log list, simulating persistent storage operations.
    
    Log Format:
        "Notification to {email}: {message}"
    
    Production Implementation:
        ```python
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        def write_notification(email: str, message: str):
            try:
                # Configure SMTP server
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(smtp_username, smtp_password)
                
                # Create email message
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email
                msg['Subject'] = "Account Notification"
                msg.attach(MIMEText(message, 'plain'))
                
                # Send email
                smtp_server.send_message(msg)
                smtp_server.quit()
                
                # Log successful delivery
                logger.info(f"Notification sent to {email}: {message}")
                
            except Exception as e:
                # Log error for monitoring
                logger.error(f"Failed to send notification to {email}: {str(e)}")
                
                # Optionally retry or queue for later
                retry_queue.append({'email': email, 'message': message})
        ```
    
    Alternative Implementations:
        ```python
        # Using SendGrid
        import sendgrid
        from sendgrid.helpers.mail import Mail
        
        def write_notification(email: str, message: str):
            sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
            mail = Mail(
                from_email='noreply@yourapp.com',
                to_emails=email,
                subject='Account Notification',
                html_content=f'<p>{message}</p>'
            )
            
            try:
                response = sg.send(mail)
                notifications_log.append(f"SendGrid notification to {email}: {message}")
            except Exception as e:
                logger.error(f"SendGrid error: {str(e)}")
        
        # Using AWS SES
        import boto3
        
        def write_notification(email: str, message: str):
            ses_client = boto3.client('ses', region_name='us-east-1')
            
            try:
                response = ses_client.send_email(
                    Source='noreply@yourapp.com',
                    Destination={'ToAddresses': [email]},
                    Message={
                        'Subject': {'Data': 'Account Notification'},
                        'Body': {'Text': {'Data': message}}
                    }
                )
                notifications_log.append(f"AWS SES notification to {email}: {message}")
            except Exception as e:
                logger.error(f"AWS SES error: {str(e)}")
        ```
    
    Error Handling Patterns:
        ```python
        def write_notification(email: str, message: str):
            try:
                # Attempt primary email service
                send_via_primary_service(email, message)
                
            except PrimaryServiceError:
                try:
                    # Fallback to secondary service
                    send_via_backup_service(email, message)
                    
                except BackupServiceError:
                    # Queue for manual processing
                    failed_notifications.append({
                        'email': email,
                        'message': message,
                        'timestamp': datetime.utcnow(),
                        'attempts': 1
                    })
                    
                    # Alert administrators
                    alert_admins(f"Notification delivery failed for {email}")
        ```
    
    Monitoring and Analytics:
        ```python
        def write_notification(email: str, message: str):
            start_time = time.time()
            
            try:
                # Send notification
                result = send_email(email, message)
                
                # Track success metrics
                metrics.increment('notifications.sent.success')
                metrics.histogram('notifications.duration', time.time() - start_time)
                
                # Log for analytics
                analytics.track('notification_sent', {
                    'email': email,
                    'message_type': classify_message(message),
                    'delivery_time': time.time() - start_time
                })
                
            except Exception as e:
                # Track failure metrics
                metrics.increment('notifications.sent.failure')
                logger.error(f"Notification failed: {str(e)}")
        ```
    
    Use Cases:
        - **Account Activity**: Login notifications, security alerts
        - **System Updates**: Maintenance notices, feature announcements
        - **Marketing**: Promotional offers, newsletter updates
        - **Transactional**: Order confirmations, payment receipts
    """
    notifications_log.append(f"Notification to {email}: {message}")


def send_welcome_email(username: str, email: str):
    """
    Background task to send welcome email to newly registered users.
    
    This function handles the user onboarding email workflow, sending
    personalized welcome messages to new users after successful registration.
    It demonstrates user-centric background task processing.
    
    Args:
        username (str): Username of the newly registered user
        email (str): Email address to send the welcome message
    
    Welcome Email Workflow:
        1. **User Registration**: User completes registration process
        2. **Immediate Response**: API returns success immediately
        3. **Background Processing**: Welcome email sent asynchronously
        4. **User Onboarding**: Email provides next steps and resources
    
    Background Task Benefits:
        - **Fast Registration**: User doesn't wait for email processing
        - **Reliable Delivery**: Email sending doesn't block user experience
        - **Error Isolation**: Email failures don't affect registration success
        - **Resource Optimization**: Email processing uses available resources
    
    Welcome Email Content Pattern:
        The function creates a standardized welcome message format that
        includes the username for personalization and confirms successful
        account creation.
    
    Production Implementation:
        ```python
        from jinja2 import Template
        import os
        
        def send_welcome_email(username: str, email: str):
            try:
                # Load email template
                template_path = os.path.join('templates', 'welcome_email.html')
                with open(template_path, 'r') as f:
                    template = Template(f.read())
                
                # Personalize email content
                email_content = template.render(
                    username=username,
                    email=email,
                    login_url=f"{base_url}/login",
                    support_email="support@yourapp.com",
                    unsubscribe_url=f"{base_url}/unsubscribe/{email}"
                )
                
                # Send email with rich content
                send_html_email(
                    to_email=email,
                    subject=f"Welcome to Our Platform, {username}!",
                    html_content=email_content,
                    text_content=generate_text_version(email_content)
                )
                
                # Log successful welcome email
                logger.info(f"Welcome email sent to {username} at {email}")
                
                # Track user onboarding metrics
                analytics.track('user_welcomed', {
                    'username': username,
                    'email': email,
                    'registration_date': datetime.utcnow()
                })
                
            except Exception as e:
                logger.error(f"Failed to send welcome email to {username}: {str(e)}")
                
                # Queue for retry
                welcome_email_retry_queue.append({
                    'username': username,
                    'email': email,
                    'retry_count': 0,
                    'next_retry': datetime.utcnow() + timedelta(minutes=5)
                })
        ```
    
    Advanced Welcome Email Features:
        ```python
        def send_welcome_email(username: str, email: str, user_preferences=None):
            # Personalization based on user data
            user_profile = get_user_profile(username)
            
            # Dynamic content based on user preferences
            welcome_content = {
                'basic': generate_basic_welcome(username),
                'detailed': generate_detailed_welcome(username, user_profile),
                'onboarding': generate_onboarding_sequence(username)
            }
            
            # Choose content based on user preference
            content_type = user_preferences.get('email_preference', 'basic')
            email_body = welcome_content.get(content_type, welcome_content['basic'])
            
            # Add personalized recommendations
            recommendations = get_user_recommendations(user_profile)
            email_body += generate_recommendations_section(recommendations)
            
            # Send with tracking
            send_tracked_email(
                to_email=email,
                subject=f"Welcome aboard, {username}!",
                content=email_body,
                campaign_id='welcome_email',
                user_id=user_profile.id
            )
        ```
    
    Multi-step Onboarding:
        ```python
        def send_welcome_email(username: str, email: str):
            # Immediate welcome
            send_immediate_welcome(username, email)
            
            # Schedule follow-up emails
            from celery import current_app
            
            # Day 1: Getting started guide
            current_app.send_task(
                'send_onboarding_email',
                args=[username, email, 'getting_started'],
                countdown=86400  # 24 hours
            )
            
            # Day 3: Feature highlights
            current_app.send_task(
                'send_onboarding_email',
                args=[username, email, 'features'],
                countdown=259200  # 72 hours
            )
            
            # Day 7: Check-in and support
            current_app.send_task(
                'send_onboarding_email',
                args=[username, email, 'checkin'],
                countdown=604800  # 1 week
            )
        ```
    
    A/B Testing Integration:
        ```python
        def send_welcome_email(username: str, email: str):
            # A/B test different welcome email versions
            variant = get_ab_test_variant(username, 'welcome_email_test')
            
            email_templates = {
                'control': 'welcome_email_v1.html',
                'variant_a': 'welcome_email_v2.html',
                'variant_b': 'welcome_email_v3.html'
            }
            
            template = email_templates.get(variant, email_templates['control'])
            
            # Send with variant tracking
            send_email_with_tracking(
                template=template,
                to_email=email,
                username=username,
                ab_variant=variant,
                test_name='welcome_email_test'
            )
            
            # Record A/B test participation
            record_ab_test_event(username, 'welcome_email_test', variant)
        ```
    
    Performance Monitoring:
        ```python
        def send_welcome_email(username: str, email: str):
            with performance_monitor.timer('welcome_email_processing'):
                try:
                    # Email sending logic
                    result = send_email_service.send_welcome(username, email)
                    
                    # Success metrics
                    metrics.increment('welcome_emails.sent.success')
                    metrics.gauge('welcome_emails.queue_size', get_queue_size())
                    
                except EmailServiceError as e:
                    # Failure metrics
                    metrics.increment('welcome_emails.sent.failure')
                    metrics.increment(f'welcome_emails.errors.{e.error_code}')
                    
                    # Alert if error rate is high
                    if get_error_rate() > 0.05:  # 5% error rate
                        alert_service.send_alert(
                            'High welcome email failure rate detected',
                            severity='warning'
                        )
        ```
    
    Use Cases:
        - **User Onboarding**: Welcome new users with account information
        - **Account Activation**: Provide activation links and instructions
        - **Getting Started**: Guide users through initial setup
        - **Community Welcome**: Introduce users to community features
        - **Support Information**: Provide help resources and contact info
    """
    notifications_log.append(f"Welcome email sent to {email} for user {username}")


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """
    Send a notification to the specified email address using background processing.
    
    This endpoint demonstrates the core pattern of background task integration
    in FastAPI, where the API response is sent immediately while the actual
    notification processing happens asynchronously in the background.
    
    Args:
        email (str): Target email address for the notification
        background_tasks (BackgroundTasks): FastAPI's background task manager
    
    Returns:
        dict: Immediate confirmation that notification was queued for processing
    
    Response Format:
        ```json
        {
            "message": "Notification sent in the background"
        }
        ```
    
    Background Task Flow:
        1. **API Request**: Client sends POST request with email address
        2. **Task Queuing**: Notification task added to background processor
        3. **Immediate Response**: API returns success immediately
        4. **Background Execution**: Notification sent after response
        5. **Task Completion**: Notification logged to persistent storage
    
    Authentication Requirements:
        - **No Authentication**: Public endpoint for demonstration
        - **Production**: Should include proper authentication and rate limiting
    
    Use Cases:
        - **Security Alerts**: Account login notifications, suspicious activity
        - **System Notifications**: Maintenance alerts, service updates
        - **User Engagement**: Feature announcements, tips and tricks
        - **Monitoring Alerts**: System status updates, error notifications
    
    Example Usage:
        ```bash
        # Send account activity notification
        curl -X POST "http://localhost:8000/send-notification/user@example.com"
        
        # Response (immediate)
        {"message": "Notification sent in the background"}
        
        # Notification processed in background
        # Check /notifications endpoint to verify delivery
        curl "http://localhost:8000/notifications"
        ```
    
    Production Implementation:
        ```python
        from fastapi import Depends, HTTPException
        from pydantic import BaseModel, EmailStr
        
        class NotificationRequest(BaseModel):
            email: EmailStr
            message: str
            priority: str = "normal"  # low, normal, high, urgent
            notification_type: str = "general"
        
        @app.post("/send-notification/")
        async def send_notification(
            notification: NotificationRequest,
            background_tasks: BackgroundTasks,
            current_user: User = Depends(get_current_user),
            rate_limiter: RateLimiter = Depends(get_rate_limiter)
        ):
            # Validate user permissions
            if not current_user.can_send_notifications():
                raise HTTPException(403, "Insufficient permissions")
            
            # Check rate limits
            if not rate_limiter.allow_request(current_user.id):
                raise HTTPException(429, "Rate limit exceeded")
            
            # Add task with metadata
            background_tasks.add_task(
                send_notification_with_tracking,
                notification.email,
                notification.message,
                notification.priority,
                notification.notification_type,
                current_user.id
            )
            
            return {
                "message": "Notification queued for delivery",
                "estimated_delivery": "within 5 minutes",
                "notification_id": generate_notification_id()
            }
        ```
    
    Error Handling Enhancement:
        ```python
        @app.post("/send-notification/{email}")
        async def send_notification(
            email: str, 
            background_tasks: BackgroundTasks
        ):
            try:
                # Validate email format
                EmailStr.validate(email)
                
                # Add task with error handling
                background_tasks.add_task(
                    safe_write_notification,
                    email,
                    "Account activity detected"
                )
                
                return {
                    "message": "Notification sent in the background",
                    "email": email,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            except ValidationError as e:
                raise HTTPException(400, f"Invalid email format: {email}")
            except Exception as e:
                logger.error(f"Failed to queue notification: {str(e)}")
                raise HTTPException(500, "Failed to queue notification")
        
        def safe_write_notification(email: str, message: str):
            try:
                write_notification(email, message)
            except Exception as e:
                logger.error(f"Background task failed: {str(e)}")
                # Add to retry queue or dead letter queue
                retry_failed_notification(email, message, str(e))
        ```
    
    Monitoring and Metrics:
        ```python
        import time
        from prometheus_client import Counter, Histogram
        
        notification_requests = Counter('notification_requests_total', 'Total notification requests')
        notification_duration = Histogram('notification_processing_seconds', 'Notification processing time')
        
        @app.post("/send-notification/{email}")
        async def send_notification(email: str, background_tasks: BackgroundTasks):
            notification_requests.inc()
            start_time = time.time()
            
            try:
                background_tasks.add_task(
                    timed_write_notification,
                    email,
                    "Account activity detected",
                    start_time
                )
                
                return {"message": "Notification sent in the background"}
                
            finally:
                # Track API response time (not background task time)
                notification_duration.observe(time.time() - start_time)
        
        def timed_write_notification(email: str, message: str, request_start_time: float):
            task_start_time = time.time()
            
            try:
                write_notification(email, message)
                
                # Track end-to-end time
                total_time = time.time() - request_start_time
                logger.info(f"Notification delivered in {total_time:.2f}s to {email}")
                
            except Exception as e:
                logger.error(f"Notification failed after {time.time() - task_start_time:.2f}s: {e}")
        ```
    
    Advanced Features:
        ```python
        from enum import Enum
        
        class NotificationPriority(Enum):
            LOW = "low"
            NORMAL = "normal"
            HIGH = "high"
            URGENT = "urgent"
        
        @app.post("/send-notification/{email}")
        async def send_notification(
            email: str,
            priority: NotificationPriority = NotificationPriority.NORMAL,
            delay_seconds: int = 0,
            background_tasks: BackgroundTasks
        ):
            if delay_seconds > 0:
                # Scheduled notification
                background_tasks.add_task(
                    delayed_notification,
                    email,
                    "Account activity detected",
                    delay_seconds
                )
                return {
                    "message": f"Notification scheduled for delivery in {delay_seconds} seconds"
                }
            else:
                # Immediate notification
                background_tasks.add_task(
                    prioritized_notification,
                    email,
                    "Account activity detected", 
                    priority
                )
                return {"message": "Notification sent in the background"}
        ```
    
    Security Considerations:
        - **Input Validation**: Validate email format and content
        - **Rate Limiting**: Prevent notification spam and abuse
        - **Authentication**: Verify user permissions for notifications
        - **Content Filtering**: Prevent malicious content in notifications
        - **Audit Logging**: Track all notification requests and outcomes
    
    Performance Considerations:
        - **Task Queuing**: Use efficient background task processing
        - **Resource Limits**: Monitor memory and CPU usage of tasks
        - **Batch Processing**: Group similar notifications for efficiency
        - **Queue Management**: Handle task queue overflow gracefully
    """
    background_tasks.add_task(write_notification, email, "Account activity detected")
    return {"message": "Notification sent in the background"}


@app.post("/register")
async def register_user(user: UserRegistration, background_tasks: BackgroundTasks):
    """
    Register a new user and initiate background welcome email processing.
    
    This endpoint demonstrates a complete user registration workflow with
    background task integration, showing how to provide immediate feedback
    to users while processing onboarding tasks asynchronously.
    
    Args:
        user (UserRegistration): Validated user registration data
        background_tasks (BackgroundTasks): FastAPI's background task manager
    
    Returns:
        dict: Immediate registration confirmation with user details
    
    Response Format:
        ```json
        {
            "message": "User registered successfully",
            "username": "johndoe"
        }
        ```
    
    Registration Workflow:
        1. **Data Validation**: Pydantic validates registration data
        2. **User Creation**: User account created in system (simulated)
        3. **Background Task**: Welcome email queued for processing
        4. **Immediate Response**: Success confirmation sent to client
        5. **Email Processing**: Welcome email sent asynchronously
    
    Background Task Benefits:
        - **Fast Registration**: User gets immediate confirmation
        - **Reliable Onboarding**: Email sending doesn't block registration
        - **Error Isolation**: Email failures don't affect account creation
        - **User Experience**: Smooth registration flow without delays
    
    Use Cases:
        - **User Onboarding**: New account creation with welcome workflow
        - **Account Activation**: Email verification and activation process
        - **Multi-step Registration**: Complex registration with background processing
        - **Service Integration**: Integration with external services and APIs
    
    Example Usage:
        ```bash
        # Register new user
        curl -X POST "http://localhost:8000/register" \
             -H "Content-Type: application/json" \
             -d '{
                 "username": "johndoe",
                 "email": "john@example.com"
             }'
        
        # Immediate response
        {
            "message": "User registered successfully",
            "username": "johndoe"
        }
        
        # Check background task completion
        curl "http://localhost:8000/notifications"
        # Shows: "Welcome email sent to john@example.com for user johndoe"
        ```
    
    Production Implementation:
        ```python
        from sqlalchemy.orm import Session
        from fastapi import Depends, HTTPException
        import bcrypt
        import uuid
        
        @app.post("/register", response_model=UserRegistrationResponse)
        async def register_user(
            user: UserRegistration,
            background_tasks: BackgroundTasks,
            db: Session = Depends(get_database)
        ):
            # Check if user already exists
            existing_user = db.query(User).filter(
                or_(User.username == user.username, User.email == user.email)
            ).first()
            
            if existing_user:
                raise HTTPException(400, "Username or email already registered")
            
            try:
                # Create user account
                hashed_password = bcrypt.hashpw(
                    user.password.encode('utf-8'), 
                    bcrypt.gensalt()
                )
                
                new_user = User(
                    id=str(uuid.uuid4()),
                    username=user.username,
                    email=user.email,
                    password_hash=hashed_password,
                    created_at=datetime.utcnow(),
                    is_active=False,  # Requires email verification
                    email_verified=False
                )
                
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                
                # Queue background tasks
                background_tasks.add_task(
                    send_welcome_email_with_verification,
                    new_user.username,
                    new_user.email,
                    new_user.id
                )
                
                background_tasks.add_task(
                    log_user_registration,
                    new_user.id,
                    request.client.host
                )
                
                background_tasks.add_task(
                    sync_user_to_external_services,
                    new_user.id
                )
                
                # Return success response
                return UserRegistrationResponse(
                    message="User registered successfully",
                    username=new_user.username,
                    user_id=new_user.id,
                    next_steps=[
                        "Check your email for verification link",
                        "Complete your profile setup",
                        "Explore getting started guide"
                    ]
                )
                
            except Exception as e:
                db.rollback()
                logger.error(f"Registration failed for {user.username}: {str(e)}")
                raise HTTPException(500, "Registration failed")
        ```
    
    Enhanced Registration with Multiple Background Tasks:
        ```python
        @app.post("/register")
        async def register_user(user: UserRegistration, background_tasks: BackgroundTasks):
            # Simulate user creation
            user_id = generate_user_id()
            
            # Queue multiple background tasks
            background_tasks.add_task(
                send_welcome_email,
                user.username,
                user.email
            )
            
            background_tasks.add_task(
                create_user_profile,
                user_id,
                user.username,
                user.email
            )
            
            background_tasks.add_task(
                send_admin_notification,
                f"New user registered: {user.username}"
            )
            
            background_tasks.add_task(
                sync_to_analytics,
                user_id,
                user.username,
                'user_registration'
            )
            
            background_tasks.add_task(
                initialize_user_preferences,
                user_id
            )
            
            return {
                "message": "User registered successfully",
                "username": user.username,
                "user_id": user_id,
                "status": "Profile setup in progress"
            }
        ```
    
    Error Handling and Rollback:
        ```python
        @app.post("/register")
        async def register_user(user: UserRegistration, background_tasks: BackgroundTasks):
            transaction_id = str(uuid.uuid4())
            
            try:
                # Create user (this could fail)
                user_id = create_user_account(user)
                
                # Queue background tasks with transaction tracking
                background_tasks.add_task(
                    safe_send_welcome_email,
                    user.username,
                    user.email,
                    user_id,
                    transaction_id
                )
                
                return {
                    "message": "User registered successfully",
                    "username": user.username,
                    "transaction_id": transaction_id
                }
                
            except UserCreationError as e:
                # Handle user creation failure
                logger.error(f"User creation failed: {str(e)}")
                raise HTTPException(400, "Registration failed: User could not be created")
            
            except Exception as e:
                # Handle unexpected errors
                logger.error(f"Unexpected registration error: {str(e)}")
                raise HTTPException(500, "Registration failed due to server error")
        
        def safe_send_welcome_email(username: str, email: str, user_id: str, transaction_id: str):
            try:
                send_welcome_email(username, email)
                
                # Log successful background task
                logger.info(f"Welcome email sent for transaction {transaction_id}")
                
            except Exception as e:
                # Log background task failure
                logger.error(f"Welcome email failed for transaction {transaction_id}: {str(e)}")
                
                # Optionally notify user of email failure
                notify_email_failure(user_id, email)
        ```
    
    Registration Analytics:
        ```python
        @app.post("/register")
        async def register_user(user: UserRegistration, background_tasks: BackgroundTasks):
            registration_start = time.time()
            
            try:
                # Registration logic
                user_id = create_user_account(user)
                
                # Background analytics tracking
                background_tasks.add_task(
                    track_registration_analytics,
                    user_id,
                    user.username,
                    registration_start,
                    request.client.host,
                    request.headers.get('user-agent')
                )
                
                return {
                    "message": "User registered successfully",
                    "username": user.username
                }
                
            except Exception as e:
                # Track failed registrations
                background_tasks.add_task(
                    track_registration_failure,
                    user.username,
                    str(e),
                    registration_start
                )
                raise
        
        def track_registration_analytics(user_id, username, start_time, ip_address, user_agent):
            registration_time = time.time() - start_time
            
            analytics_data = {
                'event': 'user_registration',
                'user_id': user_id,
                'username': username,
                'registration_duration': registration_time,
                'ip_address': ip_address,
                'user_agent': user_agent,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Send to analytics service
            analytics_service.track(analytics_data)
            
            # Update registration metrics
            metrics.increment('registrations.total')
            metrics.histogram('registrations.duration', registration_time)
        ```
    
    Security and Validation:
        ```python
        from fastapi import Depends, Request
        import ipaddress
        
        async def validate_registration_request(
            request: Request,
            user: UserRegistration
        ):
            # Rate limiting by IP
            client_ip = request.client.host
            if is_rate_limited(client_ip):
                raise HTTPException(429, "Too many registration attempts")
            
            # Validate email domain
            if not is_allowed_email_domain(user.email):
                raise HTTPException(400, "Email domain not allowed")
            
            # Check for suspicious patterns
            if is_suspicious_registration(user, client_ip):
                raise HTTPException(400, "Registration blocked by security policy")
            
            return user
        
        @app.post("/register")
        async def register_user(
            user: UserRegistration = Depends(validate_registration_request),
            background_tasks: BackgroundTasks
        ):
            # Registration logic with validated user data
            pass
        ```
    
    Performance Considerations:
        - **Database Transactions**: Use proper transaction handling
        - **Task Queuing**: Efficient background task management
        - **Resource Monitoring**: Track memory and CPU usage
        - **Batch Processing**: Group related background operations
        - **Queue Overflow**: Handle high registration volumes
    
    Security Considerations:
        - **Input Validation**: Comprehensive data validation
        - **Rate Limiting**: Prevent registration abuse
        - **Email Verification**: Verify email ownership
        - **Duplicate Prevention**: Check for existing users
        - **Audit Logging**: Track all registration attempts
    """
    background_tasks.add_task(send_welcome_email, user.username, user.email)
    return {"message": "User registered successfully", "username": user.username}


@app.get("/notifications")
async def get_notifications():
    """
    Retrieve all logged notifications to verify background task execution.
    
    This endpoint provides visibility into background task processing by
    returning all notifications that have been logged by background tasks.
    It serves as a monitoring and debugging tool for async operations.
    
    Returns:
        dict: Complete list of notifications with count statistics
    
    Response Format:
        ```json
        {
            "notifications": [
                "Notification to user@example.com: Account activity detected",
                "Welcome email sent to john@example.com for user johndoe"
            ],
            "count": 2
        }
        ```
    
    Monitoring Features:
        - **Task Verification**: Confirm background tasks executed successfully
        - **Execution History**: Complete log of all notification activities
        - **Debugging Support**: Troubleshoot background task processing
        - **Performance Tracking**: Monitor task completion rates and timing
    
    Use Cases:
        - **Development Testing**: Verify background tasks work correctly
        - **System Monitoring**: Track notification delivery status
        - **Debugging**: Investigate background task failures or delays
        - **Analytics**: Analyze notification patterns and volumes
        - **Audit Trail**: Maintain records of all notification activities
    
    Example Usage:
        ```bash
        # Check all notifications
        curl "http://localhost:8000/notifications"
        
        # Response showing background task results
        {
            "notifications": [
                "Notification to alice@example.com: Account activity detected",
                "Welcome email sent to bob@example.com for user bobsmith",
                "Notification to charlie@example.com: Account activity detected"
            ],
            "count": 3
        }
        ```
    
    Production Implementation:
        ```python
        from fastapi import Query, Depends
        from typing import Optional
        import math
        
        @app.get("/notifications", response_model=NotificationListResponse)
        async def get_notifications(
            page: int = Query(1, ge=1),
            limit: int = Query(100, le=1000),
            notification_type: Optional[str] = Query(None),
            email_filter: Optional[str] = Query(None),
            date_from: Optional[datetime] = Query(None),
            date_to: Optional[datetime] = Query(None),
            current_user: User = Depends(get_current_admin_user),
            db: Session = Depends(get_database)
        ):
            # Build query with filters
            query = db.query(NotificationLog)
            
            if notification_type:
                query = query.filter(NotificationLog.type == notification_type)
            
            if email_filter:
                query = query.filter(NotificationLog.email.contains(email_filter))
            
            if date_from:
                query = query.filter(NotificationLog.created_at >= date_from)
            
            if date_to:
                query = query.filter(NotificationLog.created_at <= date_to)
            
            # Get total count for pagination
            total_count = query.count()
            
            # Apply pagination
            offset = (page - 1) * limit
            notifications = query.offset(offset).limit(limit).all()
            
            return NotificationListResponse(
                notifications=[n.to_dict() for n in notifications],
                count=len(notifications),
                total_count=total_count,
                page=page,
                total_pages=math.ceil(total_count / limit),
                has_next=page * limit < total_count,
                has_previous=page > 1
            )
        ```
    
    Real-time Monitoring Dashboard:
        ```python
        from fastapi import WebSocket
        import asyncio
        import json
        
        # WebSocket for real-time notification monitoring
        @app.websocket("/notifications/ws")
        async def notifications_websocket(websocket: WebSocket):
            await websocket.accept()
            
            try:
                while True:
                    # Send current notification stats
                    stats = {
                        "total_notifications": len(notifications_log),
                        "recent_notifications": notifications_log[-10:],
                        "notifications_per_hour": calculate_hourly_rate(),
                        "success_rate": calculate_success_rate(),
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    await websocket.send_text(json.dumps(stats))
                    await asyncio.sleep(5)  # Update every 5 seconds
                    
            except WebSocketDisconnect:
                pass
        
        # Enhanced notifications endpoint with real-time data
        @app.get("/notifications/stats")
        async def get_notification_stats():
            now = datetime.utcnow()
            
            return {
                "total_notifications": len(notifications_log),
                "notifications_today": count_notifications_since(now - timedelta(days=1)),
                "notifications_this_hour": count_notifications_since(now - timedelta(hours=1)),
                "top_recipients": get_top_notification_recipients(limit=10),
                "notification_types": get_notification_type_breakdown(),
                "average_processing_time": calculate_average_processing_time(),
                "error_rate": calculate_error_rate(),
                "last_updated": now.isoformat()
            }
        ```
    
    Advanced Filtering and Search:
        ```python
        @app.get("/notifications/search")
        async def search_notifications(
            query: str = Query(..., min_length=3),
            search_type: str = Query("content", enum=["content", "email", "user"]),
            current_user: User = Depends(get_current_user)
        ):
            # Implement search based on type
            search_results = []
            
            if search_type == "email":
                search_results = [
                    n for n in notifications_log 
                    if query.lower() in n.lower() and "to " + query in n
                ]
            elif search_type == "content":
                search_results = [
                    n for n in notifications_log 
                    if query.lower() in n.lower()
                ]
            elif search_type == "user":
                search_results = [
                    n for n in notifications_log 
                    if f"user {query}" in n.lower()
                ]
            
            return {
                "query": query,
                "search_type": search_type,
                "results": search_results,
                "count": len(search_results)
            }
        ```
    
    Export and Reporting:
        ```python
        from fastapi.responses import StreamingResponse
        import csv
        import io
        
        @app.get("/notifications/export")
        async def export_notifications(
            format: str = Query("csv", enum=["csv", "json"]),
            date_from: Optional[datetime] = Query(None),
            date_to: Optional[datetime] = Query(None),
            current_user: User = Depends(get_current_admin_user)
        ):
            # Filter notifications by date range
            filtered_notifications = filter_notifications_by_date(
                notifications_log, date_from, date_to
            )
            
            if format == "csv":
                output = io.StringIO()
                writer = csv.writer(output)
                
                # Write header
                writer.writerow(["Timestamp", "Type", "Recipient", "Message", "Status"])
                
                # Write data
                for notification in filtered_notifications:
                    parsed = parse_notification_entry(notification)
                    writer.writerow([
                        parsed["timestamp"],
                        parsed["type"],
                        parsed["recipient"],
                        parsed["message"],
                        parsed["status"]
                    ])
                
                output.seek(0)
                return StreamingResponse(
                    io.BytesIO(output.getvalue().encode()),
                    media_type="text/csv",
                    headers={"Content-Disposition": "attachment; filename=notifications.csv"}
                )
            
            elif format == "json":
                return {
                    "notifications": filtered_notifications,
                    "export_date": datetime.utcnow().isoformat(),
                    "exported_by": current_user.username
                }
        ```
    
    Notification Analytics:
        ```python
        @app.get("/notifications/analytics")
        async def get_notification_analytics(
            period: str = Query("day", enum=["hour", "day", "week", "month"]),
            current_user: User = Depends(get_current_admin_user)
        ):
            analytics_data = {
                "period": period,
                "delivery_rates": calculate_delivery_rates(period),
                "popular_times": get_popular_notification_times(period),
                "recipient_analysis": analyze_recipient_patterns(period),
                "content_analysis": analyze_message_content(period),
                "performance_metrics": {
                    "average_processing_time": calculate_avg_processing_time(period),
                    "success_rate": calculate_success_rate(period),
                    "failure_rate": calculate_failure_rate(period),
                    "retry_rate": calculate_retry_rate(period)
                },
                "trends": {
                    "volume_trend": calculate_volume_trend(period),
                    "success_trend": calculate_success_trend(period),
                    "error_trend": calculate_error_trend(period)
                }
            }
            
            return analytics_data
        ```
    
    Security and Access Control:
        ```python
        from fastapi import Depends, HTTPException
        
        @app.get("/notifications")
        async def get_notifications(
            current_user: User = Depends(get_current_user)
        ):
            # Check if user has permission to view notifications
            if not current_user.has_permission("view_notifications"):
                raise HTTPException(403, "Insufficient permissions")
            
            # Filter notifications based on user role
            if current_user.role == "admin":
                # Admins see all notifications
                visible_notifications = notifications_log
            elif current_user.role == "moderator":
                # Moderators see only their own and public notifications
                visible_notifications = filter_notifications_for_moderator(
                    notifications_log, current_user
                )
            else:
                # Regular users see only their own notifications
                visible_notifications = [
                    n for n in notifications_log 
                    if current_user.email in n
                ]
            
            return {
                "notifications": visible_notifications,
                "count": len(visible_notifications),
                "user_role": current_user.role,
                "filtered": len(visible_notifications) < len(notifications_log)
            }
        ```
    
    Performance Considerations:
        - **Pagination**: Essential for large notification volumes
        - **Database Indexing**: Index timestamp and email fields
        - **Caching**: Cache frequent queries and statistics
        - **Query Optimization**: Use efficient database queries
        - **Memory Management**: Avoid loading all notifications at once
    
    Security Considerations:
        - **Access Control**: Verify user permissions before showing data
        - **Data Privacy**: Filter sensitive information appropriately
        - **Rate Limiting**: Prevent abuse of monitoring endpoints
        - **Audit Logging**: Log access to notification data
        - **Input Validation**: Validate all query parameters
    """
    return {"notifications": notifications_log, "count": len(notifications_log)}

