import os
from datetime import datetime
from jinja2 import Template
import base64
import io
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from flask import current_app

def generate_monthly_html_report(report_data):
    """
    Generate a comprehensive monthly HTML report for user parking activity
    
    Args:
        report_data (dict): Dictionary containing:
            - user: User object
            - month_year: String like "January 2024"
            - total_bookings: Integer
            - total_cost: Float
            - most_used_lot: Tuple (lot_name, count)
            - lot_usage: Dict {lot_name: count}
            - reservations: List of Reservation objects
    
    Returns:
        str: HTML content of the report
    """
    try:
        # Generate charts if data available
        chart_data = {}
        if report_data['lot_usage']:
            chart_data['usage_chart'] = _generate_usage_chart(report_data['lot_usage'])
            chart_data['cost_trend'] = _generate_cost_trend_chart(report_data['reservations'])
        
        # Prepare additional statistics
        stats = _calculate_detailed_stats(report_data['reservations'])
        
        # Load and render HTML template
        html_content = _render_report_template({
            **report_data,
            'charts': chart_data,
            'detailed_stats': stats,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        })
        
        return html_content
        
    except Exception as e:
        current_app.logger.error(f"Error generating HTML report: {str(e)}")
        return _generate_error_report(str(e))

def _generate_usage_chart(lot_usage):
    """Generate parking lot usage pie chart"""
    try:
        plt.figure(figsize=(8, 6))
        plt.style.use('seaborn-v0_8')
        
        lots = list(lot_usage.keys())
        counts = list(lot_usage.values())
        
        colors = plt.cm.Set3(range(len(lots)))
        
        plt.pie(counts, labels=lots, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Parking Lot Usage Distribution', fontsize=14, fontweight='bold')
        plt.axis('equal')
        
        # Convert to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        
        chart_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{chart_base64}"
        
    except Exception as e:
        current_app.logger.error(f"Error generating usage chart: {str(e)}")
        return None

def _generate_cost_trend_chart(reservations):
    """Generate daily cost trend chart"""
    try:
        if not reservations:
            return None
            
        # Group reservations by date
        daily_costs = {}
        for reservation in reservations:
            if reservation.parking_timestamp and reservation.parking_cost:
                date_key = reservation.parking_timestamp.strftime('%Y-%m-%d')
                daily_costs[date_key] = daily_costs.get(date_key, 0) + reservation.parking_cost
        
        if not daily_costs:
            return None
            
        # Sort by date
        sorted_dates = sorted(daily_costs.keys())
        costs = [daily_costs[date] for date in sorted_dates]
        
        plt.figure(figsize=(12, 6))
        plt.style.use('seaborn-v0_8')
        
        plt.plot(range(len(sorted_dates)), costs, marker='o', linewidth=2, markersize=6)
        plt.title('Daily Parking Costs Trend', fontsize=14, fontweight='bold')
        plt.xlabel('Days in Month')
        plt.ylabel('Cost ($)')
        plt.grid(True, alpha=0.3)
        
        # Format x-axis
        plt.xticks(range(0, len(sorted_dates), max(1, len(sorted_dates)//10)), 
                  [date.split('-')[2] for date in sorted_dates[::max(1, len(sorted_dates)//10)]])
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        
        chart_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return f"data:image/png;base64,{chart_base64}"
        
    except Exception as e:
        current_app.logger.error(f"Error generating cost trend chart: {str(e)}")
        return None

def _calculate_detailed_stats(reservations):
    """Calculate detailed statistics from reservations"""
    stats = {
        'avg_duration': 0,
        'total_duration': 0,
        'avg_cost_per_hour': 0,
        'peak_usage_day': 'N/A',
        'weekend_vs_weekday': {'weekend': 0, 'weekday': 0}
    }
    
    if not reservations:
        return stats
    
    total_duration_hours = 0
    duration_count = 0
    day_usage = {}
    
    for reservation in reservations:
        # Calculate duration
        if reservation.parking_timestamp and reservation.leaving_timestamp:
            duration = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600
            total_duration_hours += duration
            duration_count += 1
            
            # Day of week analysis
            day_name = reservation.parking_timestamp.strftime('%A')
            day_usage[day_name] = day_usage.get(day_name, 0) + 1
            
            # Weekend vs weekday
            if day_name in ['Saturday', 'Sunday']:
                stats['weekend_vs_weekday']['weekend'] += 1
            else:
                stats['weekend_vs_weekday']['weekday'] += 1
    
    # Calculate averages
    if duration_count > 0:
        stats['avg_duration'] = round(total_duration_hours / duration_count, 2)
        stats['total_duration'] = round(total_duration_hours, 2)
        
        total_cost = sum(r.parking_cost for r in reservations if r.parking_cost)
        if total_duration_hours > 0:
            stats['avg_cost_per_hour'] = round(total_cost / total_duration_hours, 2)
    
    # Peak usage day
    if day_usage:
        stats['peak_usage_day'] = max(day_usage.items(), key=lambda x: x[1])[0]
    
    return stats

def _render_report_template(data):
    """Render the HTML template with data"""
    
    template_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monthly Parking Report - {{ month_year }}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fa;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .content {
            padding: 30px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .chart-container {
            text-align: center;
            margin: 20px 0;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .reservations-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .reservations-table th,
        .reservations-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .reservations-table th {
            background-color: #667eea;
            color: white;
            font-weight: 600;
        }
        .reservations-table tr:hover {
            background-color: #f5f5f5;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        .highlight {
            background: linear-gradient(120deg, #a8e6cf 0%, #dcedc1 100%);
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        @media (max-width: 600px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .container {
                margin: 10px;
            }
            body {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 Monthly Parking Report</h1>
            <p>{{ month_year }} | {{ user.username }}</p>
        </div>
        
        <div class="content">
            <!-- Summary Statistics -->
            <div class="section">
                <h2>📊 Summary Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{{ total_bookings }}</div>
                        <div class="stat-label">Total Bookings</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${{ "%.2f"|format(total_cost) }}</div>
                        <div class="stat-label">Total Cost</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ "%.1f"|format(detailed_stats.avg_duration) }}h</div>
                        <div class="stat-label">Avg Duration</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${{ "%.2f"|format(detailed_stats.avg_cost_per_hour) }}</div>
                        <div class="stat-label">Cost per Hour</div>
                    </div>
                </div>
            </div>

            {% if most_used_lot %}
            <div class="highlight">
                <strong>🏆 Most Used Parking Lot:</strong> {{ most_used_lot[0] }} ({{ most_used_lot[1] }} visits)
            </div>
            {% endif %}

            <!-- Charts Section -->
            {% if charts.usage_chart %}
            <div class="section">
                <h2>📈 Usage Analytics</h2>
                <div class="chart-container">
                    <img src="{{ charts.usage_chart }}" alt="Parking Lot Usage Distribution">
                </div>
            </div>
            {% endif %}

            {% if charts.cost_trend %}
            <div class="section">
                <h2>💰 Cost Trends</h2>
                <div class="chart-container">
                    <img src="{{ charts.cost_trend }}" alt="Daily Cost Trend">
                </div>
            </div>
            {% endif %}

            <!-- Detailed Statistics -->
            <div class="section">
                <h2>📋 Detailed Insights</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{{ detailed_stats.peak_usage_day }}</div>
                        <div class="stat-label">Peak Usage Day</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ detailed_stats.weekend_vs_weekday.weekend }}</div>
                        <div class="stat-label">Weekend Bookings</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ detailed_stats.weekend_vs_weekday.weekday }}</div>
                        <div class="stat-label">Weekday Bookings</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{{ "%.1f"|format(detailed_stats.total_duration) }}h</div>
                        <div class="stat-label">Total Duration</div>
                    </div>
                </div>
            </div>

            <!-- Recent Reservations -->
            {% if reservations %}
            <div class="section">
                <h2>🎫 Recent Reservations</h2>
                <table class="reservations-table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Parking Lot</th>
                            <th>Duration</th>
                            <th>Cost</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for reservation in reservations[:10] %}
                        <tr>
                            <td>{{ reservation.parking_timestamp.strftime('%m/%d') if reservation.parking_timestamp else 'N/A' }}</td>
                            <td>{{ reservation.parking_spot.parking_lot.prime_location_name }}</td>
                            <td>
                                {% if reservation.leaving_timestamp and reservation.parking_timestamp %}
                                    {{ "%.1f"|format((reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600) }}h
                                {% else %}
                                    Active
                                {% endif %}
                            </td>
                            <td>${{ "%.2f"|format(reservation.parking_cost) if reservation.parking_cost else '0.00' }}</td>
                            <td>
                                {% if reservation.leaving_timestamp %}
                                    ✅ Completed
                                {% else %}
                                    🅿️ Active
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% if reservations|length > 10 %}
                <p><em>Showing 10 most recent reservations out of {{ reservations|length }} total.</em></p>
                {% endif %}
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Report generated on {{ generated_at }}</p>
            <p>Vehicle Parking Management System | MAD II Project</p>
        </div>
    </div>
</body>
</html>
    """
    
    template = Template(template_html)
    return template.render(**data)

def _generate_error_report(error_message):
    """Generate a simple error report"""
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #d32f2f;">Report Generation Error</h2>
        <p>Sorry, there was an error generating your monthly report.</p>
        <p><strong>Error:</strong> {error_message}</p>
        <p>Please contact support if this issue persists.</p>
    </body>
    </html>
    """

def generate_simple_html_report(title, content, user_name=None):
    """
    Generate a simple HTML report with basic styling
    
    Args:
        title (str): Report title
        content (str): HTML content
        user_name (str): Optional user name
    
    Returns:
        str: HTML content
    """
    template_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
            .header {{ background: #667eea; color: white; padding: 20px; border-radius: 5px; }}
            .content {{ padding: 20px; background: #f9f9f9; margin-top: 20px; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{title}</h1>
            {f'<p>Generated for: {user_name}</p>' if user_name else ''}
        </div>
        <div class="content">
            {content}
        </div>
        <footer style="margin-top: 20px; text-align: center; color: #666;">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </body>
    </html>
    """
    return template_html