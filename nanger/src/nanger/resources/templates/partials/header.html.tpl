<div id="header">
    <h1>${out_none value=title xml_escape=True /}</h1>
    <div class="links">
        ${if item=area value="home" operator=eq}
            <a href="${out_none value=base_path /}index" class="active">home</a>
        ${else /}
            <a href="${out_none value=base_path /}index">home</a>
        ${/if}
        //
        ${if item=area value="plugins" operator=eq}
            <a href="${out_none value=base_path /}plugins" class="active">plugins</a>
        ${else /}
            <a href="${out_none value=base_path /}plugins">plugins</a>
        ${/if}
        //
        ${if item=area value="console" operator=eq}
            <a href="${out_none value=base_path /}console" class="active">console</a>
        ${else /}
            <a href="${out_none value=base_path /}console">console</a>
        ${/if}
        //
        ${if item=area value="about" operator=eq}
            <a href="${out_none value=base_path /}about" class="active">about</a>
        ${else /}
            <a href="${out_none value=base_path /}about">about</a>
        ${/if}
    </div>
    ${if item=section value=None operator=neq}
        ${include file_value=section /}
    ${/if}
</div>
