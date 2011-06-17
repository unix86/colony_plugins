<div id="overlay"></div>
<div id="notification-area">
    <div id="notification-area-contents"></div>
</div>
<div id="header">
    <div id="logo"></div>
    <div id="account-area-container">
        <ul>
            <li>
                <a id="account-description">${out_none value=session_user_information.username /} @ ${out_none value=session_user_information.company.name /}</a>
                <div id="account-float-panel" class="float-panel">
                    <div class="float-panel-arrow"></div>
                    <div class="float-panel-content">
                        <img src="${out_none value=base_path /}resources/images/dummy-photo.png" height="64" width="64" alt="" />
                        <h1>${out_none value=session_user_information.username /}</h1>
                        <h2>${out_none value=session_user_information.company.name /}</h2>
                        <a href="#">Editar Perfil</a>
                        <a href="#">Upgrade</a>
                    </div>
                </div>
            </li>
            <li><a href="${out_none value=base_path /}logout">Logout</a></li>
            <li><a href="">My Colony</a></li>
            <li><a href="">Help</a></li>
        </ul>
    </div>
    <div id="menu-bar" class="menu-area-container">
        <ul>
            ${foreach item=menu_item_value key=menu_item_name from=menu_items}
                <li>
                    <a id="${out_none value=menu_item_name /}">${out_none value=menu_item_name.capitalize /}</a>
                </li>
            ${/foreach}
            <li><a id="help">Help</a></li>
        </ul>
        <div id="menu-bar-search-field" class="search-field">
             <input class="text" type="text"/>
             <div class="search-button"></div>
        </div>
    </div>
    ${foreach item=menu_item_value key=menu_item_name from=menu_items}
       <div id="${out_none value=menu_item_name /}-menu" class="drop-menu">
        <ul>
            ${foreach item=menu_item_item from=menu_item_value}
                <li>
                    <a href="#${out_none value=menu_item_item.address /}">${out_none value=menu_item_item.target /}</a>
                </li>
            ${/foreach}
        </ul>
    </div>
    ${/foreach}
    <div id="help-menu" class="drop-menu">
        <ul>
            <li><a href="#dashboard">About</a></li>
            <li><a href="#search">Search</a></li>
        </ul>
    </div>
</div>
<div id="filter"></div>
<div id="loading-message"></div>
<div id="environment-variables">
    <div id="base-path">${out_none value=base_path /}</div>
    <div id="ajax-submit">${out_none value=ajax_submit /}</div>
</div>
