<?php
/**
 * Plugin Name: Local Business Toolkit
 * Description: Displays verified business contact details and opening hours.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_01_local_business_toolkit_render($attributes = []) {
    $attributes = shortcode_atts([
        'business_name' => '',
        'phone' => '',
        'hours' => ''
    ], $attributes, 'adib_01_local-business-toolkit');
    $html = '<section class="adib_01_local_business_toolkit-component"><h2>Local Business Toolkit</h2><dl>';
    if ($attributes['business_name'] !== '') { $html .= '<dt>Business Name</dt><dd>' . esc_html($attributes['business_name']) . '</dd>'; }
    if ($attributes['phone'] !== '') { $html .= '<dt>Phone</dt><dd>' . esc_html($attributes['phone']) . '</dd>'; }
    if ($attributes['hours'] !== '') { $html .= '<dt>Hours</dt><dd>' . esc_html($attributes['hours']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_01_local-business-toolkit', 'adib_01_local_business_toolkit_render');

function adib_01_local_business_toolkit_assets() {
    $css = '.adib_01_local_business_toolkit-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_01_local_business_toolkit-component label{display:block;margin:.8rem 0}'
         . '.adib_01_local_business_toolkit-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_01_local_business_toolkit-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_01_local_business_toolkit-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_01_local_business_toolkit', false, [], '1.0.0');
    wp_enqueue_style('adib_01_local_business_toolkit');
    wp_add_inline_style('adib_01_local_business_toolkit', $css);
}
add_action('wp_enqueue_scripts', 'adib_01_local_business_toolkit_assets');
