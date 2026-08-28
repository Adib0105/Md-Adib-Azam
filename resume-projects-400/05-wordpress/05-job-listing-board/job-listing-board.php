<?php
/**
 * Plugin Name: Job Listing Board
 * Description: Collects a sanitized job application reference.
 * Version: 1.0.0
 * Author: Md Adib Azam
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
    exit;
}

function adib_05_job_listing_board_render($attributes = []) {
    $values = [];
    $notice = '';
    if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['adib_05_job_listing_board_nonce']) && wp_verify_nonce(sanitize_text_field(wp_unslash($_POST['adib_05_job_listing_board_nonce'])), 'adib_05_job_listing_board_submit')) {
        $values['candidate_name'] = isset($_POST['adib_05_job_listing_board_candidate_name']) ? sanitize_text_field(wp_unslash($_POST['adib_05_job_listing_board_candidate_name'])) : '';
        $values['email'] = isset($_POST['adib_05_job_listing_board_email']) ? sanitize_email(wp_unslash($_POST['adib_05_job_listing_board_email'])) : '';
        $values['role'] = isset($_POST['adib_05_job_listing_board_role']) ? sanitize_text_field(wp_unslash($_POST['adib_05_job_listing_board_role'])) : '';
        $values['resume_url'] = isset($_POST['adib_05_job_listing_board_resume_url']) ? esc_url_raw(wp_unslash($_POST['adib_05_job_listing_board_resume_url'])) : '';
        $notice = '<p role="status">Request validated for review. No personal data was stored by this demo plugin.</p>';
    }
    $html = '<section class="adib_05_job_listing_board-component"><h2>Job Listing Board</h2>' . $notice . '<form method="post">';
    $html .= wp_nonce_field('adib_05_job_listing_board_submit', 'adib_05_job_listing_board_nonce', true, false);
    $html .= '<label>Candidate Name<input name="adib_05_job_listing_board_candidate_name" type="date" required></label>';
    $html .= '<label>Email<input name="adib_05_job_listing_board_email" type="email" required></label>';
    $html .= '<label>Role<input name="adib_05_job_listing_board_role" type="text" required></label>';
    $html .= '<label>Resume Url<input name="adib_05_job_listing_board_resume_url" type="url" required></label>';
    $html .= '<button type="submit">Submit</button></form></section>';
    return $html;
}
add_shortcode('adib_05_job-listing-board', 'adib_05_job_listing_board_render');

function adib_05_job_listing_board_assets() {
    $css = '.adib_05_job_listing_board-component{max-width:760px;padding:1.5rem;border:1px solid #dbe4f0;border-radius:1rem}'
         . '.adib_05_job_listing_board-component label{display:block;margin:.8rem 0}'
         . '.adib_05_job_listing_board-component input{display:block;width:100%;max-width:34rem;padding:.65rem}'
         . '.adib_05_job_listing_board-component button{padding:.7rem 1.1rem;cursor:pointer}'
         . '.adib_05_job_listing_board-component dt{font-weight:700;margin-top:.75rem}';
    wp_register_style('adib_05_job_listing_board', false, [], '1.0.0');
    wp_enqueue_style('adib_05_job_listing_board');
    wp_add_inline_style('adib_05_job_listing_board', $css);
}
add_action('wp_enqueue_scripts', 'adib_05_job_listing_board_assets');
