<?php
/**
 * Plugin Name: Affiliate Disclosure Box
 * Description: Renders a reusable affiliate disclosure box.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_20_affiliate_disclosure_box_render($attributes = []) {
    $attributes = shortcode_atts([
        'relationship' => '',
        'merchant' => '',
        'policy_url' => ''
    ], $attributes, 'adib_20_affiliate-disclosure-box');
    $html = '<section class="adib_20_affiliate_disclosure_box-component"><h2>Affiliate Disclosure Box</h2><dl>';
    if ($attributes['relationship'] !== '') { $html .= '<dt>Relationship</dt><dd>' . esc_html($attributes['relationship']) . '</dd>'; }
    if ($attributes['merchant'] !== '') { $html .= '<dt>Merchant</dt><dd>' . esc_html($attributes['merchant']) . '</dd>'; }
    if ($attributes['policy_url'] !== '') { $html .= '<dt>Policy Url</dt><dd>' . esc_html($attributes['policy_url']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_20_affiliate-disclosure-box', 'adib_20_affiliate_disclosure_box_render');

function adib_20_affiliate_disclosure_box_assets() {
    $css = '.adib_20_affiliate_disclosure_box-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_20_affiliate_disclosure_box-component label{display:block;margin:.8rem 0}'
         . '.adib_20_affiliate_disclosure_box-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_20_affiliate_disclosure_box-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_20_affiliate_disclosure_box-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_20_affiliate_disclosure_box', false, [], '1.0.0');
    wp_enqueue_style('adib_20_affiliate_disclosure_box');
    wp_add_inline_style('adib_20_affiliate_disclosure_box', $css);
}
add_action('wp_enqueue_scripts', 'adib_20_affiliate_disclosure_box_assets');
