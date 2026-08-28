<?php
/**
 * Plugin Name: Digital Agency Lead Form
 * Description: Collects and sanitizes an agency lead without storing private data.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_02_digital_agency_lead_form_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_02_digital_agency_lead_form_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_02_digital_agency_lead_form_nonce'])), 'adib_02_digital_agency_lead_form_submit')) {
        $values['name'] = isset($_POST['adib_02_digital_agency_lead_form_name']) ? sanitize_text_field(wp_unslash($_POST['adib_02_digital_agency_lead_form_name'])) : '';
        $values['email'] = isset($_POST['adib_02_digital_agency_lead_form_email']) ? sanitize_email(wp_unslash($_POST['adib_02_digital_agency_lead_form_email'])) : '';
        $values['service'] = isset($_POST['adib_02_digital_agency_lead_form_service']) ? sanitize_text_field(wp_unslash($_POST['adib_02_digital_agency_lead_form_service'])) : '';
        $values['budget'] = isset($_POST['adib_02_digital_agency_lead_form_budget']) ? sanitize_text_field(wp_unslash($_POST['adib_02_digital_agency_lead_form_budget'])) : '';
        $notice = '<p role="status">Request validated for review. No personal data was stored by this demo plugin.</p>';
    }
    $html = '<section class="adib_02_digital_agency_lead_form-component"><h2>Digital Agency Lead Form</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_02_digital_agency_lead_form_submit', 'adib_02_digital_agency_lead_form_nonce', true, false);
    $html .= '<label>Name<input name="adib_02_digital_agency_lead_form_name" type="text" required></label>';
    $html .= '<label>Email<input name="adib_02_digital_agency_lead_form_email" type="email" required></label>';
    $html .= '<label>Service<input name="adib_02_digital_agency_lead_form_service" type="text" required></label>';
    $html .= '<label>Budget<input name="adib_02_digital_agency_lead_form_budget" type="text" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_02_digital-agency-lead-form', 'adib_02_digital_agency_lead_form_render');

function adib_02_digital_agency_lead_form_assets() {
    $css = '.adib_02_digital_agency_lead_form-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_02_digital_agency_lead_form-component label{display:block;margin:.8rem 0}'
         . '.adib_02_digital_agency_lead_form-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_02_digital_agency_lead_form-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_02_digital_agency_lead_form-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_02_digital_agency_lead_form', false, [], '1.0.0');
    wp_enqueue_style('adib_02_digital_agency_lead_form');
    wp_add_inline_style('adib_02_digital_agency_lead_form', $css);
}
add_action('wp_enqueue_scripts', 'adib_02_digital_agency_lead_form_assets');
