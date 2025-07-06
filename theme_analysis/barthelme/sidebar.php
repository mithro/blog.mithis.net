	<div id="primary" class="sidebar">
		<ul>
<?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar() ) : // Begin Widgets; displays widgets or default contents below ?>

<?php if ( !is_front_page() || is_paged() ) { // Displays a home link everywhere except the home page ?>
			<li id="home-link">
				<h3><a href="<?php bloginfo('home') ?>" title="<?php echo _wp_specialchars(get_bloginfo('name'), 1) ?>"><?php _e('Home', 'barthelme'); ?></a></h3>
			</li>
<?php } ?>

<?php wp_list_pages('title_li=<h3>'.__('Pages').'</h3>&sort_column=menu_order' ) ?>

			<li id="categories">
				<h3><?php _e('Categories', 'barthelme'); ?></h3>
				<ul>
<?php wp_list_categories('orderby=name&hierarchical=1&title_li=') ?>

				</ul>
			</li>

			<li id="tag-cloud">
				<h3><?php _e('Tags', 'barthelme') ?></h3>
				<p><?php wp_tag_cloud() ?></p>
			</li>

<?php wp_list_bookmarks('title_before=<h3>&title_after=</h3>') ?>

			<li id="feed-links">
				<h3><?php _e('RSS Feeds', 'barthelme') ?></h3>
				<ul>
					<li><a href="<?php bloginfo('rss2_url') ?>" title="<?php echo _wp_specialchars(get_bloginfo('name'), 1) ?> RSS 2.0 Feed" rel="alternate" type="application/rss+xml"><?php _e('All posts', 'barthelme') ?></a></li>
					<li><a href="<?php bloginfo('comments_rss2_url') ?>" title="<?php echo _wp_specialchars(bloginfo('name'), 1) ?> Comments RSS 2.0 Feed" rel="alternate" type="application/rss+xml"><?php _e('All comments', 'barthelme') ?></a></li>
				</ul>
			</li>

			<li id="meta">
				<h3><?php _e('Meta', 'barthelme') ?></h3>
				<ul>
					<?php wp_register() ?>
					<li><?php wp_loginout() ?></li>
					<?php wp_meta() // Do not remove; helps plugins work ?>
				</ul>
			</li>

			<li id="search">
				<h3><label for="s"><?php _e('Blog Search', 'barthelme') ?></label></h3>
				<form id="searchform" method="get" action="<?php bloginfo('home') ?>">
					<div>
						<input id="s" name="s" type="text" value="<?php the_search_query() ?>" size="10" />
						<input id="searchsubmit" name="searchsubmit" type="submit" value="<?php _e('Search', 'barthelme') ?>" />
					</div>
				</form>
			</li>
<?php endif; // End Widgets ?>

		</ul>
	</div>
