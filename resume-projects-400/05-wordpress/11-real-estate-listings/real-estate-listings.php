<?php
/**
 * Plugin Name: Real Estate Listings
 * Description: Displays responsive real-estate listing cards.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_11_real_estate_listings_render($attributes = []) {
    $attributes = shortcode_atts([
        'property' => '',
        'location' => '',
        'price' => ''
    ], $attributes, 'adib_11_real-estate-listings');
    $html = '<section class="adib_11_real_estate_listings-component"><h2>Real Estate Listings</h2><dl>';
    if ($attributes['property'] !== '') { $html .= '<dt>Property</dt><dd>' . esc_html($attributes['property']) . '</dd>'; }
    if ($attributes['location'] !== '') { $html .= '<dt>Location</dt><dd>' . esc_html($attributes['location']) . '</dd>'; }
    if ($attributes['price'] !== '') { $html .= '<dt>Price</dt><dd>' . esc_html($attributes['price']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_11_real-estate-listings', 'adib_11_real_estate_listings_render');

function adib_11_real_estate_listings_assets() {
    $css = '.adib_11_real_estate_listings-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_11_real_estate_listings-component label{display:block;margin:.8rem 0}'
         . '.adib_11_real_estate_listings-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_11_real_estate_listings-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_11_real_estate_listings-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_11_real_estate_listings', false, [], '1.0.0');
    wp_enqueue_style('adib_11_real_estate_listings');
    wp_add_inline_style('adib_11_real_estate_listings', $css);
}
add_action('wp_enqueue_scripts', 'adib_11_real_estate_listings_assets');
