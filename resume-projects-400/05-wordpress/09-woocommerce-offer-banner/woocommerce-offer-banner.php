<?php
/**
 * Plugin Name: WooCommerce Offer Banner
 * Description: Shows a dismissible WooCommerce promotion banner.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_09_woocommerce_offer_banner_render($attributes = []) {
    $attributes = shortcode_atts([
        'message' => '',
        'coupon' => '',
        'expires' => ''
    ], $attributes, 'adib_09_woocommerce-offer-banner');
    $html = '<section class="adib_09_woocommerce_offer_banner-component"><h2>WooCommerce Offer Banner</h2><dl>';
    if ($attributes['message'] !== '') { $html .= '<dt>Message</dt><dd>' . esc_html($attributes['message']) . '</dd>'; }
    if ($attributes['coupon'] !== '') { $html .= '<dt>Coupon</dt><dd>' . esc_html($attributes['coupon']) . '</dd>'; }
    if ($attributes['expires'] !== '') { $html .= '<dt>Expires</dt><dd>' . esc_html($attributes['expires']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_09_woocommerce-offer-banner', 'adib_09_woocommerce_offer_banner_render');

function adib_09_woocommerce_offer_banner_assets() {
    $css = '.adib_09_woocommerce_offer_banner-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_09_woocommerce_offer_banner-component label{display:block;margin:.8rem 0}'
         . '.adib_09_woocommerce_offer_banner-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_09_woocommerce_offer_banner-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_09_woocommerce_offer_banner-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_09_woocommerce_offer_banner', false, [], '1.0.0');
    wp_enqueue_style('adib_09_woocommerce_offer_banner');
    wp_add_inline_style('adib_09_woocommerce_offer_banner', $css);
}
add_action('wp_enqueue_scripts', 'adib_09_woocommerce_offer_banner_assets');
