--[[
  Ink filter for reveal.js decks.
  GENERATED from brand/tokens.json by scripts/build_brand.py. Do not edit.

  1. Section dividers. A slide background is painted by reveal.js outside the
     <section>, so CSS on the section cannot colour it. Every heading marked
     `.ink-dark` (or the old `.sdaia-dark`) gets the ink background, and any
     gradient or image from an older theme is dropped.

  2. Light / night mode. Adds ink-mode.html (the toggle) to the page. For
     every image whose .dark twin exists beside it (fig_x.png ->
     fig_x.dark.png), adds data-dark-src and registers the twin as a resource
     so Quarto copies it to the output.
]]

local INK = "#16181D"

local function file_exists(path)
  local f = io.open(path, "rb")
  if f then f:close() return true end
  return false
end

local function input_dir()
  if quarto and quarto.doc and quarto.doc.input_file then
    return pandoc.path.directory(quarto.doc.input_file)
  end
  return "."
end

local function dark_twin(src)
  if src:match("^%a[%w+.-]*:") or src:match("^/") then return nil end  -- URLs, absolute paths
  local stem, ext = src:match("^(.*)%.(%w+)$")
  if not stem or stem:match("%.dark$") then return nil end
  local twin = stem .. ".dark." .. ext
  if file_exists(pandoc.path.join({ input_dir(), twin })) then return twin end
  return nil
end

function Header(el)
  if el.classes:includes("ink-dark") or el.classes:includes("sdaia-dark") then
    el.attributes["background-gradient"] = nil
    el.attributes["background-image"] = nil
    el.attributes["background-color"] = INK
    return el
  end
end

function Image(el)
  local twin = dark_twin(el.src)
  if twin then
    el.attributes["data-dark-src"] = twin
    el.attributes["data-light-src"] = el.src
    if quarto and quarto.doc and quarto.doc.add_resource then
      -- add_resource resolves relative paths against this filter's folder,
      -- so hand it the twin's absolute path.
      quarto.doc.add_resource(pandoc.path.join({ input_dir(), twin }))
    end
    return el
  end
end

function Meta(meta)
  if quarto and quarto.doc and quarto.doc.include_file then
    quarto.doc.include_file("after-body", "ink-mode.html")
  end
  return meta
end
