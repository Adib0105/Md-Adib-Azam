<?php
/**
 * Plugin Name: Clinic Appointment Request
 * Description: Collects a clinic appointment request.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_14_clinic_appointment_request_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_14_clinic_appointment_request_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_14_clinic_appointment_request_nonce'])), 'adib_14_clinic_appointment_request_submit')) {
        $values['patient_name'] = isset($_POST['adib_14_clinic_appointment_request_patient_name']) ? sanitize_text_field(wp_unslash($_POST['adib_14_clinic_appointment_request_patient_name'])) : '';
        $values['email'] = isset($_POST['adib_14_clinic_appointment_request_email']) ? sanitize_email(wp_unslash($_POST['adib_14_clinic_appointment_request_email'])) : '';
        $values['department'] = isset($_POST['adib_14_clinic_appointment_request_department']) ? sanitize_text_field(wp_unslash($_POST['adib_14_clinic_appointment_request_department'])) : '';
        $values['preferred_date'] = isset($_POST['adib_14_clinic_appointment_request_preferred_date']) ? sanitize_text_field(wp_unslash($_POST['adib_14_clinic_appointment_request_preferred_date'])) : '';
        $notice = '<p role="status">Request validated for review. No personal data was stored by this demo plugin.</p>';
    }
    $html = '<section class="adib_14_clinic_appointment_request-component"><h2>Clinic Appointment Request</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_14_clinic_appointment_request_submit', 'adib_14_clinic_appointment_request_nonce', true, false);
    $html .= '<label>Patient Name<input name="adib_14_clinic_appointment_request_patient_name" type="text" required></label>';
    $html .= '<label>Email<input name="adib_14_clinic_appointment_request_email" type="email" required></label>';
    $html .= '<label>Department<input name="adib_14_clinic_appointment_request_department" type="text" required></label>';
    $html .= '<label>Preferred Date<input name="adib_14_clinic_appointment_request_preferred_date" type="date" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_14_clinic-appointment-request', 'adib_14_clinic_appointment_request_render');

function adib_14_clinic_appointment_request_assets() {
    $css = '.adib_14_clinic_appointment_request-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_14_clinic_appointment_request-component label{display:block;margin:.8rem 0}'
         . '.adib_14_clinic_appointment_request-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_14_clinic_appointment_request-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_14_clinic_appointment_request-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_14_clinic_appointment_request', false, [], '1.0.0');
    wp_enqueue_style('adib_14_clinic_appointment_request');
    wp_add_inline_style('adib_14_clinic_appointment_request', $css);
}
add_action('wp_enqueue_scripts', 'adib_14_clinic_appointment_request_assets');
