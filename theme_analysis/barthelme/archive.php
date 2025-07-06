<?php get_header() ?>

	<div id="container">
		<div id="content" class="hfeed">

<?php the_post() ?>
<?php if ( is_day() ) : ?>
			<h2 class="page-title"><span class="archive-meta"><?php _e('<span class="meta-sep">{</span> Daily Archives <span class="meta-sep">}</span>', 'barthelme') ?></span> <?php the_time(__('l, F Y', 'barthelme')) ?></h2>
<?php elseif ( is_month() ) : ?>
			<h2 class="page-title"><span class="archive-meta"><?php _e('<span class="meta-sep">{</span> Monthly Archives <span class="meta-sep">}</span>', 'barthelme') ?></span> <?php the_time(__('F Y', 'barthelme')) ?></h2>
<?php elseif ( is_year() ) : ?>
			<h2 class="page-title"><span class="archive-meta"><?php _e('<span class="meta-sep">{</span> Yearly Archives <span class="meta-sep">}</span>', 'barthelme') ?></span> <?php the_time(__('Y', 'barthelme')) ?></h2>
<?php elseif ( is_author() ) : ?>
			<h2 class="page-title"><span class="archive-meta"><?php _e('<span class="meta-sep">{</span> Author Archives <span class="meta-sep">}</span>', 'barthelme') ?></span> <?php barthelme_author_hCard() ?></h2>
			<div class="archive-meta"><?php if ( !(''== $authordata->user_description) ) : echo apply_filters('archive_meta', $authordata->user_description); endif; ?></div>
<?php elseif ( is_category() ) : ?>
			<h2 class="page-title"><span class="archive-meta"><?php _e('<span class="meta-sep">{</span> Category Archives <span class="meta-sep">}</span>', 'barthelme') ?></span> <?php echo single_cat_title(); ?></h2>
			<div class="archive-meta"><?php if ( !(''== category_description()) ) : echo apply_filters('archive_meta', category_description()); endif; ?></div>
<?php elseif ( is_tag() ) : ?>
			<h2 class="page-title"><span class="archive-meta"><?php _e('<span class="meta-sep">{</span> Tag Archives <span class="meta-sep">}</span>', 'barthelme') ?></span> <?php single_tag_title(); ?></h2>
			<div class="archive-meta"></div>
<?php elseif ( isset($_GET['paged']) && !empty($_GET['paged']) ) : ?>
			<h2 class="page-title"><span class="archive-meta"><?php _e('<span class="meta-sep">{</span> Blog Archives <span class="meta-sep">}</span>', 'barthelme') ?></span> <?php printf(__('%1$s Archives', 'barthelme'), _wp_specialchars(get_the_title(), 'double') ) ?></h2>
<?php endif; ?>
<?php rewind_posts() ?>
<?php while ( have_posts() ) : the_post(); ?>

			<div id="post-<?php the_ID() ?>" class="<?php barthelme_post_class() ?>">
				<div class="post-container">
					<div class="post-content">
						<h3 class="entry-title"><a href="<?php the_permalink() ?>" title="<?php printf(__('Permalink to %s', 'barthelme'), _wp_specialchars(get_the_title(), 1)) ?>" rel="bookmark"><?php the_title() ?></a></h3>
						<div class="entry-content">
<?php the_excerpt('<span class="more-link">'.__('Continue reading &rsaquo;', 'barthelme').'</span>') ?>

<?php if ( !is_tag() ) { echo the_tags(__('<span class="tag-links">Tagged ', 'barthelme'), ", ", "</span>"); } else { $other_tags = barthelme_other_tags(', '); printf(__('<span class="tag-links">Also tagged %s</span>', 'barthelme'), $other_tags); } ?>

						</div>
					</div>
				</div>
				<div class="entry-meta">
					<span class="entry-date"><abbr class="published" title="<?php the_time('Y-m-d\TH:i:sO'); ?>"><?php unset($previousday); printf(__('%1$s', 'barthelme'), the_date('Y m d', false)) ?></abbr></span>
					<?php if ( !is_author() ) : ?><?php barthelme_author_link(); ?><?php endif; ?>
					<span class="entry-category"><?php if ( !is_category() ) { echo the_category('<br/>'); } else { $other_cats = barthelme_other_cats('<br/>'); echo $other_cats; } ?></span>
					<span class="entry-comments"><?php comments_popup_link(__('Comments (0)', 'barthelme'), __('Comments (1)', 'barthelme'), __('Comments (%)', 'barthelme')) ?></span>
<?php edit_post_link(__('Edit', 'barthelme'), "\t\t\t\t\t<span class='entry-edit'>", "</span>\n"); ?>
				</div>
			</div><!-- .post -->

<?php endwhile ?>

			<div id="nav-below" class="navigation">
				<div class="nav-previous"><?php next_posts_link(__('&laquo; Older posts', 'barthelme')) ?></div>
				<div class="nav-next"><?php previous_posts_link(__('Newer posts &raquo;', 'barthelme')) ?></div>
			</div>

		</div><!-- #content .hfeed -->
	</div><!-- #container -->

<?php get_sidebar() ?>
<?php get_footer() ?>