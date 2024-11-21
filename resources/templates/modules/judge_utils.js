<script>
    // utilities
    function strict_match_ignore_trailing_newline (S, T) {
        let is_str = true;
        if (typeof S !== "string") is_str = false;
        if (typeof T !== "string") is_str = false;
        if (!is_str) {
            console.error("This is not string!");
            console.error(S);
            console.error(T);
            return false;
        }

        return S.trim() === T.trim();
    }

    function normalize_newlines_to_lf (S) {
        if (typeof S !== "string") {
            console.error("This is not string!");
            return "";
        }

        return S.replace(/\r\n|\n|\r/g, "\n");
    }

    function is_file_selected (form_element) {
        if (form_element.value === "") return false;
        return true;
    }
</script>
