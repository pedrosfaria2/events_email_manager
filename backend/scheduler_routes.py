from flask import Blueprint, jsonify, request
from .scheduler_thread import get_scheduled_jobs, enable_job, disable_job
from .email_checker import check_emails

scheduler_bp = Blueprint('scheduler', __name__)

@scheduler_bp.route('/scheduled-jobs', methods=['GET'])
def list_scheduled_jobs():
    jobs = get_scheduled_jobs()
    return jsonify(jobs)

@scheduler_bp.route('/scheduled-jobs/<int:job_id>/enable', methods=['POST'])
def enable_scheduled_job(job_id):
    enable_job(job_id)
    return jsonify({'status': 'enabled'})

@scheduler_bp.route('/scheduled-jobs/<int:job_id>/disable', methods=['POST'])
def disable_scheduled_job(job_id):
    disable_job(job_id)
    return jsonify({'status': 'disabled'})

@scheduler_bp.route('/check-emails', methods=['GET'])
def manual_check_emails():
    try:
        check_emails()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
