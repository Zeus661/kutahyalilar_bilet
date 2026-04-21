<script lang="ts">
    import { PUBLIC_API_BASE_URL } from "$env/static/public";

    let email = $state("");
    let password = $state("");
    let confirmPassword = $state("");
    let error = $state("");
    let loading = $state(false);

    let mismatch = $derived(
        password !== confirmPassword && confirmPassword.length > 0,
    );

    async function onSubmit(event: SubmitEvent) {
        event.preventDefault();

        error = "";

        if (!email || !password || !confirmPassword) {
            error = "Tüm alanlar zorunludur.";
            return;
        }

        if (password.length < 8) {
            error = "Şifre en az 8 karakter olmalıdır.";
            return;
        }

        if (password !== confirmPassword) {
            error = "Şifreler eşleşmiyor.";
            return;
        }

        loading = true;

        try {
            const regRes = await fetch(
                `${PUBLIC_API_BASE_URL}/api/v1/auth/register`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password }),
                },
            );

            if (!regRes.ok) {
                if (regRes.status === 409) {
                    error = "Bu e-posta adresi zaten kayıtlı.";
                    return;
                }
                const err = await regRes
                    .json()
                    .catch(() => ({ detail: "Kayıt başarısız." }));
                error = err.detail ?? "Kayıt başarısız.";
                return;
            }

            const loginRes = await fetch(
                `${PUBLIC_API_BASE_URL}/api/v1/auth/login`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email, password }),
                },
            );

            if (!loginRes.ok) {
                const err = await loginRes
                    .json()
                    .catch(() => ({ detail: "Giriş başarısız." }));
                error =
                    err.detail ??
                    "Kayıt tamamlandı, fakat otomatik giriş başarısız.";
                return;
            }

            const { access_token } = await loginRes.json();
            document.cookie = `jwt=${access_token}; Path=/; SameSite=Lax`;

            window.location.href = "/";
        } catch {
            error = "Sunucu hatası.";
        } finally {
            loading = false;
        }
    }
</script>

<svelte:head>
    <title>Kayıt Ol — Kütahyalılar</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
    <h1 class="mb-8 text-center text-3xl font-bold text-kutahya-dark">
        Kayıt Ol
    </h1>

    {#if error}
        <div
            class="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
        >
            {error}
        </div>
    {/if}

    <form onsubmit={onSubmit} class="space-y-5">
        <div>
            <label
                for="email"
                class="mb-1 block text-sm font-medium text-gray-700"
                >E-posta</label
            >
            <input
                id="email"
                name="email"
                type="email"
                bind:value={email}
                required
                class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red"
            />
        </div>

        <div>
            <label
                for="password"
                class="mb-1 block text-sm font-medium text-gray-700"
                >Şifre</label
            >
            <input
                id="password"
                name="password"
                type="password"
                bind:value={password}
                minlength="8"
                required
                class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red"
            />
        </div>

        <div>
            <label
                for="confirmPassword"
                class="mb-1 block text-sm font-medium text-gray-700"
                >Şifre Tekrar</label
            >
            <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                bind:value={confirmPassword}
                minlength="8"
                required
                class="w-full rounded-lg border-gray-300 focus:border-kutahya-red focus:ring-kutahya-red {mismatch
                    ? 'border-red-500'
                    : ''}"
            />
            {#if mismatch}
                <p class="mt-1 text-xs text-red-500">Şifreler eşleşmiyor.</p>
            {/if}
        </div>

        <button
            type="submit"
            disabled={mismatch || loading}
            class="w-full rounded-lg bg-kutahya-red py-2.5 font-semibold text-white transition hover:bg-red-700 disabled:opacity-50"
        >
            {#if loading}Kaydediliyor...{:else}Kayıt Ol{/if}
        </button>
    </form>

    <p class="mt-6 text-center text-sm text-kutahya-muted">
        Zaten hesabınız var mı?
        <a
            href="/auth/login"
            class="font-medium text-kutahya-red hover:underline">Giriş Yap</a
        >
    </p>
</div>
