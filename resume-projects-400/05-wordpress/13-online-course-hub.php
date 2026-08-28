<?php
/** Plugin Name: Online Course Hub
 * Description: Portfolio WordPress shortcode project.
 * Version: 1.0.0
 * Author: Md Adib Azam */
if (!defined('ABSPATH')) exit;
function adib_project_13_shortcode($atts) {
  $a = shortcode_atts(['title' => 'Online Course Hub', 'cta' => 'Get started'], $atts);
  return '<section class="adib-card"><h2>'.esc_html($a['title']).'</h2><p>Fast, responsive and accessible WordPress solution.</p><a href="#contact">'.esc_html($a['cta']).'</a></section>';
}
add_shortcode('adib_project_13', 'adib_project_13_shortcode');
function adib_project_13_assets() { wp_add_inline_style('wp-block-library', '.adib-card{padding:2rem;border-radius:1rem;background:#081a33;color:#fff} .adib-card a{color:#60a5fa}'); }
add_action('wp_enqueue_scripts', 'adib_project_13_assets');
