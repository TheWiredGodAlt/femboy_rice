# end-4/dots-hyprland no Arch: só pacman + GitHub do autor

Guia copia-e-cola em português. Variante "hardcore" do guia anterior: **elimina 100% do uv/PyPI** (inclusive o Python 3.12 baixado pelo uv). Auditado contra o mesmo commit `2f2a376` do branch `main` (11/10/2026). Hyprland 0.55 (configuração em Lua).

## 0. Resposta curta

**Sim, dá.** Depois desta variante, a única coisa executada no seu sistema que não vem assinada pelo pacman é o código do próprio GitHub do end-4 (o repo dos dots, um submódulo e uma fonte). Nada de AUR, nada de PyPI, nada de binário de Python gerenciado pelo uv.

O truque: quase tudo que o venv PyPI fornece existe como pacote oficial `python-*` do Arch. Só **duas** dependências não têm equivalente oficial (`materialyoucolor` e `kde-material-you-colors`), e elas alimentam só duas funcionalidades acessórias — que esta variante desliga de propósito (seção 2).

## 1. O que muda em relação ao guia anterior

| Item | Guia anterior | Esta variante |
| --- | --- | --- |
| ~33 pacotes PyPI (versões fixas, **sem hashes**) no venv `~/.local/state/quickshell/.venv` | instalados por `uv pip install` | **eliminados**; substituídos por pacotes `python-*` oficiais |
| Python 3.12 baixado pelo uv (binário de terceiros) | usado pelo venv | **eliminado**; usa o `python` do sistema (pacote oficial) |
| pacotes `uv` e `clang` (só serviam para montar o venv) | instalados | **removidos da lista** |
| venv em `~/.local/state/quickshell/.venv` | cheio de wheels do PyPI | vira um **venv "casca"** criado localmente com `python3 -m venv --system-site-packages --without-pip`: zero código baixado, só symlinks para o Python do sistema |
| wrappers `*-venv.sh` e shebangs especiais | inalterados | **inalterados também** — a casca de venv os satisfaz sem nenhum patch |

Por que a casca de venv funciona: os scripts do rice (`find_regions.py`, `thumbgen.py`, `token_from_key.py`, `scheme_for_image.py`, `hyprconfigurator.py`) são chamados por wrappers que fazem `source $ILLOGICAL_IMPULSE_VIRTUAL_ENV/bin/activate`. Com `--system-site-packages`, o Python do venv enxerga os pacotes instalados pelo pacman. Nenhum wrapper precisa de patch.

## 2. O que deixa de funcionar (decisão consciente)

Estas duas dependências só existem no PyPI e foram cortadas:

| Dependência PyPI | Funcionalidade perdida |
| --- | --- |
| `materialyoucolor` | cores do terminal derivadas do wallpaper (kitty + sequências ANSI), via `generate_colors_material.py` → `applycolor.sh` |
| `kde-material-you-colors` | tematização automática de apps Qt/KDE (Dolphin etc.) pela cor do wallpaper |

**O que continua funcionando:** todo o theming principal é feito pelo `matugen` (pacote oficial): shell Quickshell, Hyprland, Hyprlock, Fuzzel e GTK3/GTK4 continuam coloridos pelo wallpaper. Também continuam: seletor de wallpaper com thumbnails, detecção de região no screenshot (OpenCV), overlay do tradutor de tela, e token do Gemini para o chat de IA. Apps Qt ficam com o esquema Breeze padrão e o terminal com as cores padrão — só perdem o "tint" do wallpaper.

Se algum dia essas duas libs entrarem nos repos oficiais, dá para reverter os 2 patches da seção 3.5 e recuperar tudo.

## 3. Passo a passo

### 3.1 Backup

```bash
cp -a ~/.config ~/.config.bak-$(date +%F)
```

O instalador também oferece backup em `~/ii-original-dots-backup`. Responda `y` quando perguntar.

### 3.2 Atualizar o sistema e checar o Hyprland

```bash
sudo pacman -Syu
pacman -Q hyprland
```

A versão precisa ser **0.55.x ou maior**. Se for menor, repita `-Syu`. Não prossiga com 0.54 ou menor: o `main` do repo usa config Lua e não carrega.

### 3.3 Instalar as dependências oficiais (com pré-voo)

Diferenças em relação ao guia anterior: **saíram** `clang` e `uv`; **entraram** `python` e os módulos Python que o rice usa, todos oficiais.

```bash
PKGS=(
  base-devel git rsync wget curl jq go-yq bc cmake ripgrep xdg-user-dirs cliphist coreutils
  cava pavucontrol-qt wireplumber pipewire-pulse libdbusmenu-gtk3 playerctl
  geoclue brightnessctl ddcutil upower wtype ydotool
  hyprland hyprsunset hypridle hyprlock hyprpicker wl-clipboard
  bluedevil gnome-keyring networkmanager plasma-nm polkit-kde-agent dolphin systemsettings
  xdg-desktop-portal xdg-desktop-portal-kde xdg-desktop-portal-gtk xdg-desktop-portal-hyprland
  gtk4 libadwaita libsoup3 libportal-gtk4 gobject-introspection
  hyprshot slurp swappy tesseract tesseract-data-eng wf-recorder
  fuzzel glib2 imagemagick songrec translate-shell libqalculate
  adw-gtk-theme breeze breeze-icons eza fish fontconfig kitty matugen starship
  ttf-jetbrains-mono-nerd ttf-material-symbols-variable noto-fonts-emoji
  quickshell qt6-5compat qt6-imageformats qt6-multimedia qt6-positioning qt6-quicktimeline
  qt6-sensors qt6-svg qt6-tools qt6-translations qt6-virtualkeyboard qt6-wayland
  kirigami kdialog syntax-highlighting
  python python-numpy opencv python-click python-loguru python-tqdm
  python-gobject python-google-auth python-requests gnome-desktop-4
)
MISSING=()
for p in ${PKGS[@]}; do pacman -Si $p >/dev/null 2>&1 || MISSING+=($p); done
echo "Fora dos repos oficiais: ${MISSING[*]:-nenhum}"
```

Se imprimir `nenhum`, instale:

```bash
sudo pacman -S --needed ${PKGS[@]}
```

Se imprimir algum nome, **pare**: não cubra o buraco com AUR.

Plugin AVIF (mesmo fallback do guia anterior):

```bash
pacman -Si qt6-avif-image-plugin >/dev/null 2>&1 && sudo pacman -S --needed qt6-avif-image-plugin || sudo pacman -S --needed kimageformats libavif
```

Mapa de quem é quem, para referência: `cv2` → `opencv`, `numpy` → `python-numpy`, `click`/`loguru`/`tqdm` → `python-click`/`python-loguru`/`python-tqdm`, `gi` → `python-gobject`, tipelib `GnomeDesktop-4.0` → `gnome-desktop-4`, `google.auth` → `python-google-auth`, `requests` → `python-requests`.

### 3.4 Clonar, fixar o commit auditado e ler o que vai rodar

```bash
mkdir -p ~/src && cd ~/src
git clone https://github.com/end-4/dots-hyprland.git
cd dots-hyprland
git checkout -b pacman-only 2f2a376fdb2ad738bf55f693dd0b474b64bb0ab8
git submodule update --init --recursive
```

Leia o que será copiado e executado:

```bash
less sdata/subcmd-install/2.setups.sh
ls -R dots/.config/hypr | less
```

### 3.5 Aplicar as substituições (5 arquivos)

Os 3 primeiros `sed` são os do guia anterior. Os 3 últimos são os novos, que removem uv/PyPI. Os números de linha (24-25, 34, 307-311) foram conferidos no commit fixado acima; o `git diff` no final mostra exatamente o que mudou — confira antes de commitar.

```bash
# 1) estilo Qt 'Darkly' (AUR) -> Breeze
sed -i 's/widgetStyle Darkly/widgetStyle breeze/' sdata/subcmd-install/2.setups.sh

# 2) kdeglobals copiado também aponta para Darkly
sed -i 's/^widgetStyle=Darkly$/widgetStyle=breeze/' dots/.config/kdeglobals

# 3) ícones: breeze-plus (AUR) -> breeze / breeze-dark (oficial)
sed -i 's/^iconslight = breeze-plus$/iconslight = breeze/; s/^iconsdark = breeze-plus-dark$/iconsdark = breeze-dark/' dots/.config/kde-material-you-colors/config.conf

# 4) NOVO: instalador não cria mais o venv uv/PyPI (2.setups.sh, linhas 24-25)
sed -i '24,25s/^/# pacman-only: /' sdata/subcmd-install/2.setups.sh

# 5) NOVO: switchwall sem PyPI — desliga theming de apps Qt/KDE (kde-material-you-colors, linha 34)
sed -i '34s/^/# pacman-only: /' dots/.config/quickshell/ii/scripts/colors/switchwall.sh

# 6) NOVO: switchwall sem PyPI — desliga theming de terminal (generate_colors_material.py + applycolor.sh, linhas 307-311)
sed -i '307,311s/^/# pacman-only: /' dots/.config/quickshell/ii/scripts/colors/switchwall.sh

git --no-pager diff
```

Esperado: 4 linhas comentadas em `switchwall.sh`+1 na linha 34 (5 no total), 3 em `2.setups.sh` (1 substituição + 2 comentários), 1 em `kdeglobals`, 2 em `config.conf`. Se o bloco 307-311 não for exatamente `source ...activate` / `python3 ...generate_colors_material.py...` / `deactivate` / `applycolor.sh`, **desfaça com `git checkout -- .` e me avise** — o commit pode ter mudado.

```bash
git commit -am 'pacman-only: sem uv/PyPI; Darkly->Breeze; breeze-plus->breeze'
```

O `matugen "${matugen_args[@]}"` na linha logo acima do bloco comentado **permanece ativo** — é ele que faz o theming principal.

### 3.6 Rodar o instalador sem a etapa de dependências

Rode como usuário normal (o script recusa root):

```bash
./setup install --skip-alldeps
```

Ele vai pedir `sudo`, oferecer backup (`y`), ajustar grupos e serviços e copiar as configs. **Não vai** criar venv, baixar Python nem tocar no PyPI. Um aviso vermelho sobre `$ILLOGICAL_IMPULSE_VIRTUAL_ENV` pode aparecer no fim: é inofensivo, a variável é definida pelo `env.lua` na sessão do Hyprland.

Ainda dentro do escopo "só o GitHub do autor": o instalador baixa a fonte **Google Sans Flex** de `github.com/end-4/google-sans-flex` (repo do próprio end-4), via `git pull` da branch main sem commit fixo, e o submódulo `rounded-polygon-qmljs` (também do end-4, commit fixado pelo `.gitmodules`). Se quiser cortar até a fonte (ela é só a fonte padrão da UI; sem ela cai na fonte do sistema), adicione antes do passo 3.6:

```bash
sed -i '227,228s/^/# pacman-only: /' sdata/subcmd-install/3.files.sh
git commit -am 'pacman-only: sem google-sans-flex'
```

### 3.7 Criar o venv "casca" (sem baixar nada)

Depois do instalador, crie o venv vazio apontando para o Python do sistema:

```bash
python3 -m venv --system-site-packages --without-pip ~/.local/state/quickshell/.venv
ls ~/.local/state/quickshell/.venv/lib/python*/site-packages/
```

O `ls` deve mostrar o diretório **vazio** — prova de que não há nenhum código de terceiros ali, só symlinks e scripts de ativação gerados localmente. Os wrappers `*-venv.sh` do rice vão usar essa casca e resolver todos os imports nos pacotes `python-*` do pacman.

### 3.8 Relogar e iniciar

Grupos novos só valem em sessão nova. Logout/login (ou reboot) e confira:

```bash
groups | tr ' ' '\n' | grep -E '^(video|i2c|input)$'
sudo modprobe i2c-dev
```

No TTY:

```bash
start-hyprland
```

`Super` + `/` lista os keybinds; `Super` + `Enter` abre o terminal; `Ctrl` + `Super` + `T` abre o seletor de wallpaper (bom teste: os thumbnails usam o venv casca + `gnome-desktop-4`).

### 3.9 Se algo estiver errado

```bash
pkill quickshell && qs -c ii
journalctl --user -b --no-pager | grep -i -E 'quickshell|qs' | tail -50
```

- **`ModuleNotFoundError: No module named 'X'`** num script do rice: falta o pacote oficial correspondente — use o mapa da 3.3 (ex.: `cv2` → `sudo pacman -S opencv`). Não instale nada via pip.
- **Thumbnails de wallpaper não aparecem:** confira `gnome-desktop-4` instalado e teste manualmente: `~/.config/quickshell/ii/scripts/thumbnails/thumbgen-venv.sh --help`.
- **Erro de QML / API inexistente:** Quickshell oficial incompatível com o commit — o plano B do guia anterior continua valendo (PKGBUILD `illogical-impulse-quickshell-git`, que compila do git upstream, sem AUR).
- **Cores do terminal/Qt não mudam com o wallpaper:** esperado — é o corte consciente da seção 2.

## 4. Inventário final: o que resta fora do pacman

1. **Repo `end-4/dots-hyprland`** — commit fixado `2f2a376`, auditado.
2. **Submódulo `rounded-polygon-qmljs`** — GitHub do próprio end-4, commit fixado pelo `.gitmodules`.
3. **Fonte Google Sans Flex** — GitHub do end-4, `git pull` sem pin (opcionalmente removível, seção 3.6).
4. **Ações privilegiadas do `./setup`**: `groupadd i2c`, `usermod -aG video,i2c,input`, `/etc/modules-load.d/i2c-dev.conf`, `systemctl enable bluetooth --now`, serviço de usuário `ydotool`. O grupo `input` lê eventos brutos de teclado/mouse; `i2c` dá acesso ao barramento I2C (brilho via DDC).
5. **Config em Lua do Hyprland executa código arbitrário** — leia `dots/.config/hypr/` (3.4).

Comparado ao guia anterior, **saíram** da lista: os ~33 pacotes PyPI sem hash e o binário de Python 3.12 gerenciado pelo uv. O risco residual é exatamente "confiar no GitHub do autor do rice" — que era o seu objetivo.

## 5. Manutenção, atualização e rollback

Sistema: `sudo pacman -Syu`. O venv casca sobrevive a atualizações; se um dia for apagado, recrie com o comando da 3.7.

Atualizar o rice (lendo antes o que mudou):

```bash
cd ~/src/dots-hyprland
git fetch origin
git log --oneline HEAD..origin/main -- sdata dots | head -40
git diff HEAD...origin/main -- sdata/uv sdata/subcmd-install dots/.config/quickshell/ii/scripts
```

Atenção especial a: `sdata/uv/requirements.in` (dependência Python nova? confira se existe `pacman -Si python-<nome>` antes de atualizar) e aos arquivos patcheados — os números de linha dos `sed` da 3.5 podem mudar de commit para commit. Depois de conferir:

```bash
git rebase origin/main   # resolve conflitos nos pontos patcheados, se houver
./setup install --skip-alldeps
```

Rollback: restaure de `~/ii-original-dots-backup` e `~/.config.bak-*`.

## 6. O que eu não consegui verificar

- Meu ambiente não tem `pacman`: a lista da 3.3 não foi testada com `pacman -S` (por isso o pré-voo com `pacman -Si`). Todos os pacotes Python adicionados foram confirmados individualmente no archlinux.org como `extra`, exceto `gnome-desktop-4`, confirmado como `extra` 51.0.
- Não subi o shell: a compatibilidade do Quickshell oficial com o commit é indício forte, sem prova.
- Os patches de linha (3.5) valem exatamente para o commit `2f2a376`.
