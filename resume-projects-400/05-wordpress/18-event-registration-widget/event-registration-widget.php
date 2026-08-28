<?php
/**
 * Plugin Name: Event Registration Widget
 * Description: Captures event registration details.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_18_event_registration_widget_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_18_event_registration_widget_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_18_event_registration_widget_nonce'])), 'adib_18_event_registration_widget_submit')) {
        $values['attendee'] = isset($_POST['adib_18_event_registration_widget_attendee']) ? sanitize_text_field(wp_unslash($_POST['adib_18_event_registration_widget_attendee'])) : '';
        $values['email'] = isset($_POST['adib_18_event_registration_widget_email']) ? sanitize_email(wp_unslash($_POST['adib_18_event_registration_widget_email'])) : '';
        $values['ticket_type'] = isset($_POST['adib_18_event_registration_widget_ticket_type']) ? sanitize_text_field(wp_unslash($_POST['adib_18_event_registration_widget_ticket_type'])) : '';
        $values['quantity'] = isset($_POST['adib_18_event_registration_widget_quantity']) ? absint(wp_unslash($_POST['adib_18_event_registration_widget_quantity'])) : '';
        $notice = '<p role="status">Request validated for review. No personal data was stored by this demo plugin.</p>';
    }
    $html = '<section class="adib_18_event_registration_widget-component"><h2>Event Registration Widget</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_18_event_registration_widget_submit', 'adib_18_event_registration_widget_nonce', true, false);
    $html .= '<label>Attendee<input name="adib_18_event_registration_widget_attendee" type="text" required></label>';
    $html .= '<label>Email<input name="adib_18_event_registration_widget_email" type="email" required></label>';
    $html .= '<label>Ticket Type<input name="adib_18_event_registration_widget_ticket_type" type="text" required></label>';
    $html .= '<label>Quantity<input name="adib_18_event_registration_widget_quantity" type="number" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_18_event-registration-widget', 'adib_18_event_registration_widget_render');

function adib_18_event_registration_widget_assets() {
    $css = '.adib_18_event_registration_widget-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_18_event_registration_widget-component label{display:block;margin:.8rem 0}'
         . '.adib_18_event_registration_widget-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_18_event_registration_widget-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_18_event_registration_widget-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_18_event_registration_widget', false, [], '1.0.0');
    wp_enqueue_style('adib_18_event_registration_widget');
    wp_add_inline_style('adib_18_event_registration_widget', $css);
}
add_action('wp_enqueue_scripts', 'adib_18_event_registration_widget_assets');
