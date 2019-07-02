;
var account_index_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });
    }
};

$(document).ready(function () {
    account_index_ops.init();
});