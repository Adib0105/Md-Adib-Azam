<?php
/**
 * Plugin Name: Multilingual Business Notice
 * Description: Displays a language-labelled business notice.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_19_multilingual_business_notice_render($attributes = []) {
    $attributes = shortcode_atts([
        'language' => '',
        'message' => '',
        'contact_url' => ''
    ], $attributes, 'adib_19_multilingual-business-notice');
    $html = '<section class="adib_19_multilingual_business_notice-component"><h2>Multilingual Business Notice</h2><dl>';
    if ($attributes['language'] !== '') { $html .= '<dt>Language</dt><dd>' . esc_html($attributes['language']) . '</dd>'; }
    if ($attributes['message'] !== '') { $html .= '<dt>Message</dt><dd>' . esc_html($attributes['message']) . '</dd>'; }
    if ($attributes['contact_url'] !== '') { $html .= '<dt>Contact Url</dt><dd>' . esc_html($attributes['contact_url']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_19_multilingual-business-notice', 'adib_19_multilingual_business_notice_render');

function adib_19_multilingual_business_notice_assets() {
    $css = '.adib_19_multilingual_business_notice-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_19_multilingual_business_notice-component label{display:block;margin:.8rem 0}'
         . '.adib_19_multilingual_business_notice-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_19_multilingual_business_notice-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_19_multilingual_business_notice-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_19_multilingual_business_notice', false, [], '1.0.0');
    wp_enqueue_style('adib_19_multilingual_business_notice');
    wp_add_inline_style('adib_19_multilingual_business_notice', $css);
}
add_action('wp_enqueue_scripts', 'adib_19_multilingual_business_notice_assets');
