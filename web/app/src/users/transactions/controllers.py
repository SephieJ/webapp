# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, session,
                   request, url_for, redirect, jsonify)
from flask_login import login_required, current_user
from app.src.users.transactions.forms import (RateTransactionForm,
                                              TransactionForm,
                                              AgreementForm)
from app.src.users.transactions import services
from app.src.users import services as user_services
from app.src.utils import helpers

UserTransactionBP = Blueprint('UserTransactionBP', __name__)


# View Transaction List (Buying)
@UserTransactionBP.route('/transactions/buying', methods=['GET', 'POST'])
@login_required
def view_buying_transactions_page():
    status = request.args.get('status')

    ba_page = '/transactions/buying?status=active'
    bc_page = '/transactions/buying?status=completed'

    sa_page = '/transactions/buying?status=active'
    sc_page = '/transactions/buying?status=completed'

    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(uid)
    buying_transactions = services.get_buying_transactions(uid,
                                                           mode=mode)
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    return render_template('users/transactions.html',
                           transaction_type='buying',
                           status=status,
                           transactions=buying_transactions,
                           user=user,
                           message_count=message_count,
                           transaction_count=transaction_count,
                           transaction_form=transaction_form,
                           ba_page=ba_page, bc_page=bc_page,
                           sa_page=sa_page, sc_page=sc_page)


# View Transaction List (Selling)
@UserTransactionBP.route('/transactions/selling', methods=['GET', 'POST'])
@login_required
def view_selling_transactions_page():
    status = request.args.get('status')

    ba_page = '/transactions/selling?status=active'
    bc_page = '/transactions/selling?status=completed'

    sa_page = '/transactions/selling?status=active'
    sc_page = '/transactions/selling?status=completed'

    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(uid)
    selling_transactions = services.get_selling_transactions(uid,
                                                             mode=mode)
    # return jsonify(selling_transactions)
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    return render_template('users/transactions.html',
                           transaction_type='selling',
                           status=status,
                           transactions=selling_transactions,
                           user=user,
                           message_count=message_count,
                           transaction_count=transaction_count,
                           transaction_form=transaction_form,
                           ba_page=ba_page, bc_page=bc_page,
                           sa_page=sa_page, sc_page=sc_page)


# View Transaction Details
@UserTransactionBP.route('/transactions/<int:transaction_id>',
                         methods=['GET', 'POST'])
@login_required
def transaction_details_page(transaction_id):
    rate_form = RateTransactionForm()
    transaction = services.get_transaction_details(current_user.id,
                                                   transaction_id)
    count_transactions = services.get_transactions(current_user.id, mode='all')
    if request.method == 'POST' and rate_form.validate_on_submit():
        sanitized_inputs = helpers.sanitize(request.form)
        rate_transaction = services.rate_transaction(current_user.id,
                                                     transaction_id,
                                                     sanitized_inputs)
        if rate_transaction.status_code == 202:
            # flash('Transaction successfully rated.', 'success')
            print rate_transaction.status_code
        else:
            # flash(rate_transaction.text, 'danger')
            print rate_transaction.status_code
    return render_template('users/view_transactions.html',
                           transaction=transaction, rate_form=rate_form,
                           count_transactions=count_transactions)


# Cancel Transaction
@UserTransactionBP.route('/transactions/<int:transaction_id>/cancel',
                         methods=['GET', 'POST'])
@login_required
def cancel_transaction_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(uid)
    buying_transactions = services.get_buying_transactions(uid,
                                                           mode=mode)
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/transactions.html',
                               transaction_type='buying',
                               status=status,
                               transactions=buying_transactions,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form)
    elif request.method == 'POST':
        if transaction_form.validate():
            cancel_transaction = services.cancel_transaction(uid,
                                                             transaction_id)
            if cancel_transaction.status_code == 202:
                # flash('Transaction successfully cancelled.', 'success')
                return redirect(url_for('.view_buying_transactions_page',
                                        tab='buying'))
            else:
                # flash(cancel_transaction.text, 'danger')
                return redirect(url_for('.view_buying_transactions_page',
                                        tab='buying'))
        else:
            return render_template('users/transactions.html',
                                   transaction_type='buying',
                                   status=status,
                                   transactions=buying_transactions,
                                   user=user,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   transaction_form=transaction_form)


# Accept Transaction
@UserTransactionBP.route('/transactions/<int:transaction_id>/accept',
                         methods=['GET', 'POST'])
@login_required
def accept_transaction_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(uid)
    selling_transactions = services.get_selling_transactions(uid,
                                                             mode=mode)
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']
    if request.method == 'GET':
        return render_template('users/transactions.html',
                               transaction_type='selling',
                               status=status,
                               transactions=selling_transactions,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form)
    elif request.method == 'POST':
        if transaction_form.validate():
            accept_transaction = services.accept_transaction(uid,
                                                             transaction_id)
            if accept_transaction.status_code == 202:
                # flash('Transaction successfully accepted.', 'success')
                return redirect(url_for('.view_selling_transactions_page',
                                        tab='selling'))
            else:
                # flash(accept_transaction.text, 'danger')
                return redirect(url_for('.view_selling_transactions_page',
                                        tab='selling'))
        else:
            return render_template('users/transactions.html',
                                   transaction_type='selling',
                                   status=status,
                                   transactions=selling_transactions,
                                   user=user,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   transaction_form=transaction_form)


# Reject Transaction
@UserTransactionBP.route('/transactions/<int:transaction_id>/reject',
                         methods=['POST'])
@login_required
def reject_transaction_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(current_user.id)
    selling_transactions = services.get_selling_transactions(uid,
                                                             mode=mode)
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if request.method == 'GET':
        return render_template('users/transactions.html',
                               transaction_type='selling',
                               status=status,
                               transactions=selling_transactions,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form)
    elif request.method == 'POST':
        if transaction_form.validate():
            reject_transaction = services.reject_transaction(uid,
                                                             transaction_id)
            if reject_transaction.status_code == 202:
                # flash('Transaction successfully rejected.', 'success')
                return redirect(url_for('.view_selling_transactions_page',
                                        tab='selling'))
            else:
                # flash(reject_transaction.text, 'danger')
                return redirect(url_for('.view_selling_transactions_page',
                                        tab='selling'))
        else:
            return render_template('users/transactions.html',
                                   transaction_type='selling',
                                   status=status,
                                   transactions=selling_transactions,
                                   user=user,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   transaction_form=transaction_form)


# Complete Transaction
@UserTransactionBP.route('/transactions/<int:transaction_id>/complete',
                         methods=['POST'])
@login_required
def complete_transaction_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(current_user.id)
    selling_transactions = services.get_selling_transactions(uid,
                                                             mode=mode)
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if request.method == 'GET':
        return render_template('users/transactions.html',
                               transaction_type='selling',
                               status=status,
                               transactions=selling_transactions,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form)
    elif request.method == 'POST':
        if transaction_form.validate():
            complete_transaction = services.complete_transaction(
                uid, transaction_id)
            if complete_transaction.status_code == 202:
                # flash('Transaction successfully completed.', 'success')
                return redirect(url_for('.view_selling_transactions_page',
                                        tab='selling'))
            else:
                # flash(complete_transaction.text, 'danger')
                return redirect(url_for('.view_selling_transactions_page',
                                        tab='selling'))
        else:
            return render_template('users/transactions.html',
                                   transaction_type='selling',
                                   status=status,
                                   transactions=selling_transactions,
                                   user=user,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   transaction_form=transaction_form)


# AJAX Transaction Rate
@UserTransactionBP.route('/transactions/<int:transaction_id>/rate',
                         methods=['GET'])
@login_required
def rate_transaction(transaction_id):
    rating = request.args.get('rating')
    message = request.args.get('message')
    rate_transaction = services.rate_transaction(current_user.id,
                                                 transaction_id, rating,
                                                 message)
    return jsonify({'status_code': rate_transaction.status_code})


# Complete Transaction
@UserTransactionBP.route('/documentations/<int:transaction_id>/complete',
                         methods=['POST'])
@login_required
def complete_documentation_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(current_user.id)
    selling_transactions = services.get_selling_transactions(uid, mode=mode)
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    if request.method == 'GET':
        return render_template('users/documentations.html',
                               transaction_type='selling',
                               status=status,
                               transactions=selling_transactions,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form)


@UserTransactionBP.route('/agreements/selling/<int:transaction_id>',
                         methods=['GET', 'POST'])
@login_required
def selling_agreement_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    # mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id

    user = user_services.get_profile(current_user.id)
    # selling_transactions = services.get_selling_transactions(uid, mode=mode)
    transaction_data = services.get_transaction_details(current_user.id,
                                                        transaction_id)

    if not transaction_data:
        return render_template('error_pages/404-orig.html')
    if current_user.id != transaction_data['seller']['id']:
        return render_template('error_pages/404-orig.html')

    count_transactions = services.get_transactions(uid, mode='all')
    transaction_form = TransactionForm()

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    for transaction in count_transactions:
        print transaction

    if request.method == 'GET':
        return render_template('users/agreements.html',
                               transaction_type='selling',
                               transactions=transaction,
                               transaction_data=transaction_data,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form,
                               transaction_id=transaction_id)


@UserTransactionBP.route('/agreements/buying/<int:transaction_id>',
                         methods=['GET', 'POST'])
@login_required
def buying_agreement_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    # mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id

    user = user_services.get_profile(current_user.id)
    # selling_transactions = services.get_selling_transactions(uid, mode=mode)
    buying_transaction = services.get_transaction_details(current_user.id,
                                                          transaction_id)
    transaction_data = services.get_transaction_details(current_user.id,
                                                        transaction_id)
    if not buying_transaction:
        return render_template('error_pages/404-orig.html')
    if current_user.id != buying_transaction['buyer']['id']:
        return render_template('error_pages/404-orig.html')
    # return jsonify(buying_transaction)
    transaction_form = TransactionForm()
    count_transactions = services.get_transactions(uid, mode='all')

    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    for transaction in count_transactions:
        print transaction

    if request.method == 'GET':
        return render_template('users/agreements.html',
                               transaction_type='buying',
                               status=status,
                               buying_transaction=buying_transaction,
                               transactions=transaction,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form,
                               transaction_id=transaction_id,
                               transaction_data=transaction_data)


@UserTransactionBP.route('/agreements/<int:transaction_id>',
                         methods=['GET', 'POST'])
@login_required
def agreements_page(transaction_id):
    transaction = services.get_transaction_details(current_user.id,
                                                   transaction_id)
    return jsonify(transaction)


# Accept Transaction
@UserTransactionBP.route('/transactions/<int:transaction_id>/gotoagreement',
                         methods=['GET', 'POST'])
@login_required
def accept_transaction_gotoagreement_page(transaction_id):
    status = request.args.get('status')
    if status is None:
        status = 'active'
    mode = 'unarchived' if status == 'active' else 'archived'
    uid = current_user.id
    user = user_services.get_profile(uid)
    selling_transactions = services.get_selling_transactions(uid,
                                                             mode=mode)
    transaction_form = TransactionForm()
    count_transactions = services.get_transactions(uid,
                                                   mode='all')
    basic_auth = session['user_basic']
    count_auth = user_services.get_count_auth(basic_auth)
    message_count = count_auth['message_count']
    transaction_count = count_auth['pending_transaction_count']

    for transaction in count_transactions:
        print transaction

    if request.method == 'GET':
        return render_template('users/transactions.html',
                               transaction_type='selling',
                               status=status,
                               transactions=selling_transactions,
                               user=user,
                               message_count=message_count,
                               transaction_count=transaction_count,
                               transaction_form=transaction_form)
    elif request.method == 'POST':
        if transaction_form.validate():
            accept_transaction = services.accept_transaction(uid,
                                                             transaction_id)
            if accept_transaction.status_code == 202:
                # flash('Transaction successfully accepted.', 'success')
                return redirect(url_for('.selling_agreement_page',
                                        transaction_id=transaction_id))
            else:
                # flash(accept_transaction.text, 'danger')
                return redirect(url_for('.selling_agreement_page',
                                        transaction_id=transaction_id))
        else:
            return render_template('users/transactions.html',
                                   transaction_type='selling',
                                   status=status,
                                   transactions=selling_transactions,
                                   user=user,
                                   message_count=message_count,
                                   transaction_count=transaction_count,
                                   transaction_form=transaction_form)


@UserTransactionBP.route('/resources/agreement/add',
                         methods=['GET', 'POST'])
@login_required
def resource_agreement_page():
    if request.method == 'POST':
        agreement_form = AgreementForm()
        if agreement_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            booking_reference_code = sanitized_inputs['booking_reference_code']
            agreement = {
                'booking_reference_code': booking_reference_code,
                'agreement_html': request.form['agreement_html'],
            }
            reource_agreement = \
                services.save_seller_resource_agreement(agreement)
    return jsonify(reource_agreement.json())


@UserTransactionBP.route('/resources/agreement/accept',
                         methods=['GET', 'POST'])
@login_required
def resource_agreement_accept_page():
    if request.method == 'POST':
        agreement_form = AgreementForm()
        if agreement_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            booking_reference_code = sanitized_inputs['booking_reference_code']
            agreement = {
                'booking_reference_code': booking_reference_code
            }
            resource_agreement = \
                services.save_buyer_resource_agreement_accept(agreement)
    return jsonify(resource_agreement.json())


@UserTransactionBP.route('/resources/agreement/edit', methods=['GET', 'POST'])
@login_required
def resource_agreement_edit_page():
    if request.method == 'POST':
        agreement_form = AgreementForm()
        if agreement_form.validate_on_submit():
            sanitized_inputs = helpers.sanitize(request.form)
            booking_reference_code = sanitized_inputs['booking_reference_code']
            agreement = {
                'booking_reference_code': booking_reference_code,
                'agreement_html': request.form['agreement_html'],
            }
            resource_agreement = services.edit_agreement(agreement)
    return jsonify(resource_agreement.json())


@UserTransactionBP.route('/get/resources/agreement/<string:reference_code>',
                         methods=['GET', 'POST'])
@login_required
def get_resource_agreement_page(reference_code):
        resource_agreement = services.get_resource_agreement(reference_code)
        return jsonify(resource_agreement.json())
