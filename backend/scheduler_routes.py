from flask import Blueprint, jsonify, request
from .scheduler_thread import get_scheduled_jobs, enable_job, disable_job

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
