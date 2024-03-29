frappe.ui.form.PrintView.prototype.setup_toolbar = function() {
	this.page.set_primary_action(__("Print"), () => this.printit(), "printer");

	this.page.add_button(__("Full Page"), () => this.render_page("/printview?"), {
		icon: "full-page",
	});

	this.page.add_button(__("PDF"), () => this.render_pdf(), { icon: "small-file" });
	this.page.add_button(__("PDF New"), () => this.render_pdf_new(), { icon: "small-file" });

	this.page.add_button(__("Refresh"), () => this.refresh_print_format(), {
		icon: "refresh",
	});

	this.page.add_action_icon(
		"file",
		() => {
			this.go_to_form_view();
		},
		"",
		__("Form")
	);
}

frappe.ui.form.PrintView.prototype.render_pdf_new = function(){
	/*var me = this;
	frappe.call({
		method: "erpnext_html_to_pdf.utils.generate_pdf",
		args: {
			"doctype": me.frm.doc.doctype,
			"name": me.frm.doc.name,
			"format": me.selected_format(),
			"no_letterhead": me.with_letterhead() ? "0" : "1",
			"letterhead": me.get_letterhead(),
			"settings": me.additional_settings,
			"_lang": me.lang_code,
		},
		freeze: true,
		callback: function(r){
			window.open(r.message, "_blank");
		}
	})*/
	this.render_page("/api/method/erpnext_html_to_pdf.utils.generate_pdf?");
}