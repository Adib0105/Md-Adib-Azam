<?php
/**
 * Plugin Name: Service Booking Form
 * Description: Captures a service booking request with a nonce.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_06_service_booking_form_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_06_service_booking_form_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_06_service_booking_form_nonce'])), 'adib_06_service_booking_form_submit')) {
        $values['customer_name'] = isset($_POST['adib_06_service_booking_form_customer_name']) ? sanitize_text_field(wp_unslash($_POST['adib_06_service_booking_form_customer_name'])) : '';
        $values['email'] = isset($_POST['adib_06_service_booking_form_email']) ? sanitize_email(wp_unslash($_POST['adib_06_service_booking_form_email'])) : '';
        $values['service'] = isset($_POST['adib_06_service_booking_form_service']) ? sanitize_text_field(wp_unslash($_POST['adib_06_service_booking_form_service'])) : '';
        $values['preferred_date'] = isset($_POST['adib_06_service_booking_form_preferred_date']) ? sanitize_text_field(wp_unslash($_POST['adib_06_service_booking_form_preferred_date'])) : '';
        $notice = '<p role="status">Request validated for review. No personal data was stored by this demo plugin.</p>';
    }
    $html = '<section class="adib_06_service_booking_form-component"><h2>Service Booking Form</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_06_service_booking_form_submit', 'adib_06_service_booking_form_nonce', true, false);
    $html .= '<label>Customer Name<input name="adib_06_service_booking_form_customer_name" type="text" required></label>';
    $html .= '<label>Email<input name="adib_06_service_booking_form_email" type="email" required></label>';
    $html .= '<label>Service<input name="adib_06_service_booking_form_service" type="text" required></label>';
    $html .= '<label>Preferred Date<input name="adib_06_service_booking_form_preferred_date" type="date" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_06_service-booking-form', 'adib_06_service_booking_form_render');

function adib_06_service_booking_form_assets() {
    $css = '.adib_06_service_booking_form-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_06_service_booking_form-component label{display:block;margin:.8rem 0}'
         . '.adib_06_service_booking_form-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_06_service_booking_form-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_06_service_booking_form-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_06_service_booking_form', false, [], '1.0.0');
    wp_enqueue_style('adib_06_service_booking_form');
    wp_add_inline_style('adib_06_service_booking_form', $css);
}
add_action('wp_enqueue_scripts', 'adib_06_service_booking_form_assets');
