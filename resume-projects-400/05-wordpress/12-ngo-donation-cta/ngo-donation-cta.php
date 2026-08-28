<?php
/**
 * Plugin Name: NGO Donation CTA
 * Description: Creates an accessible NGO donation call-to-action.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_12_ngo_donation_cta_render($attributes = []) {
    $attributes = shortcode_atts([
        'campaign' => '',
        'goal' => '',
        'donate_url' => ''
    ], $attributes, 'adib_12_ngo-donation-cta');
    $html = '<section class="adib_12_ngo_donation_cta-component"><h2>NGO Donation CTA</h2><dl>';
    if ($attributes['campaign'] !== '') { $html .= '<dt>Campaign</dt><dd>' . esc_html($attributes['campaign']) . '</dd>'; }
    if ($attributes['goal'] !== '') { $html .= '<dt>Goal</dt><dd>' . esc_html($attributes['goal']) . '</dd>'; }
    if ($attributes['donate_url'] !== '') { $html .= '<dt>Donate Url</dt><dd>' . esc_html($attributes['donate_url']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_12_ngo-donation-cta', 'adib_12_ngo_donation_cta_render');

function adib_12_ngo_donation_cta_assets() {
    $css = '.adib_12_ngo_donation_cta-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_12_ngo_donation_cta-component label{display:block;margin:.8rem 0}'
         . '.adib_12_ngo_donation_cta-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_12_ngo_donation_cta-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_12_ngo_donation_cta-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_12_ngo_donation_cta', false, [], '1.0.0');
    wp_enqueue_style('adib_12_ngo_donation_cta');
    wp_add_inline_style('adib_12_ngo_donation_cta', $css);
}
add_action('wp_enqueue_scripts', 'adib_12_ngo_donation_cta_assets');
