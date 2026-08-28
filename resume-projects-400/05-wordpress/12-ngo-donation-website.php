<?php
/** Plugin Name: NGO Donation Website
 * Description: Portfolio WordPress shortcode project.
 * Version: 1.0.0
 * Author: Md Adib Azam */
if (!defined('ABSPATH')) exit;
function adib_project_12_shortcode($atts) {
  $a = shortcode_atts(['title' => 'NGO Donation Website', 'cta' => 'Get started'], $atts);
  return '<section class="adib-card"><h2>'.esc_html($a['title']).'</h2><p>Fast, responsive and accessible WordPress solution.</p><a href="#contact">'.esc_html($a['cta']).'</a></section>';
}
add_shortcode('adib_project_12', 'adib_project_12_shortcode');
function adib_project_12_assets() { wp_add_inline_style('wp-block-library', '.adib-card{padding:2rem;border-radius:1rem;background:#081a33;color:#fff} .adib-card a{color:#60a5fa}'); }
add_action('wp_enqueue_scripts', 'adib_project_12_assets');
