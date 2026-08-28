<?php
/**
 * Plugin Name: Membership Content Gate
 * Description: Shows gated-content guidance based on login status.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_17_membership_content_gate_render($attributes = []) {
    $attributes = shortcode_atts([
        'message' => '',
        'login_url' => '',
        'member_role' => ''
    ], $attributes, 'adib_17_membership-content-gate');
    if (is_user_logged_in()) {
        return '<section class="adib_17_membership_content_gate-component"><h2>Membership Content Gate</h2><p>' . esc_html($attributes['message']) . '</p></section>';
    }
    return '<section class="adib_17_membership_content_gate-component"><h2>Members only</h2><p>' . esc_html($attributes['message']) . '</p><a href="' . esc_url($attributes['login_url']) . '">Log in</a></section>';
}
add_shortcode('adib_17_membership-content-gate', 'adib_17_membership_content_gate_render');

function adib_17_membership_content_gate_assets() {
    $css = '.adib_17_membership_content_gate-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_17_membership_content_gate-component label{display:block;margin:.8rem 0}'
         . '.adib_17_membership_content_gate-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_17_membership_content_gate-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_17_membership_content_gate-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_17_membership_content_gate', false, [], '1.0.0');
    wp_enqueue_style('adib_17_membership_content_gate');
    wp_add_inline_style('adib_17_membership_content_gate', $css);
}
add_action('wp_enqueue_scripts', 'adib_17_membership_content_gate_assets');
