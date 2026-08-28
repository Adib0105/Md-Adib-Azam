<?php
/**
 * Plugin Name: Education Course Cards
 * Description: Renders accessible course cards from shortcode attributes.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_03_education_course_cards_render($attributes = []) {
    $attributes = shortcode_atts([
        'course' => '',
        'level' => '',
        'duration' => ''
    ], $attributes, 'adib_03_education-course-cards');
    $html = '<section class="adib_03_education_course_cards-component"><h2>Education Course Cards</h2><dl>';
    if ($attributes['course'] !== '') { $html .= '<dt>Course</dt><dd>' . esc_html($attributes['course']) . '</dd>'; }
    if ($attributes['level'] !== '') { $html .= '<dt>Level</dt><dd>' . esc_html($attributes['level']) . '</dd>'; }
    if ($attributes['duration'] !== '') { $html .= '<dt>Duration</dt><dd>' . esc_html($attributes['duration']) . '</dd>'; }
    $html .= '</dl></section>';
    return $html;
}
add_shortcode('adib_03_education-course-cards', 'adib_03_education_course_cards_render');

function adib_03_education_course_cards_assets() {
    $css = '.adib_03_education_course_cards-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_03_education_course_cards-component label{display:block;margin:.8rem 0}'
         . '.adib_03_education_course_cards-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_03_education_course_cards-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_03_education_course_cards-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_03_education_course_cards', false, [], '1.0.0');
    wp_enqueue_style('adib_03_education_course_cards');
    wp_add_inline_style('adib_03_education_course_cards', $css);
}
add_action('wp_enqueue_scripts', 'adib_03_education_course_cards_assets');
