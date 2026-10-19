from django import forms
from .models import HeritageItem

# Shared Tailwind CSS classes for form widgets with Plum (#381932) and Milk (#FFF3E6)
INPUT_CLASSES = (
    'w-full px-4 py-3 pl-11 border-[1.5px] border-[#381932]/20 rounded-xl '
    'text-[#381932] text-sm bg-white placeholder-gray-400 outline-none '
    'transition-all duration-200 '
    'focus:border-[#381932] focus:ring-[3px] focus:ring-[#381932]/15 focus:bg-[#FFF3E6]/30'
)

INPUT_CLASSES_NO_ICON = (
    'w-full px-4 py-3 border-[1.5px] border-[#381932]/20 rounded-xl '
    'text-[#381932] text-sm bg-white placeholder-gray-400 outline-none '
    'transition-all duration-200 '
    'focus:border-[#381932] focus:ring-[3px] focus:ring-[#381932]/15 focus:bg-[#FFF3E6]/30'
)

TEXTAREA_CLASSES = (
    'w-full px-4 py-3 border-[1.5px] border-[#381932]/20 rounded-xl '
    'text-[#381932] text-sm bg-white placeholder-gray-400 outline-none '
    'transition-all duration-200 resize-y min-h-[130px] '
    'focus:border-[#381932] focus:ring-[3px] focus:ring-[#381932]/15 focus:bg-[#FFF3E6]/30'
)


class HeritageItemForm(forms.ModelForm):
    class Meta:
        model = HeritageItem
        fields = ['title', 'category', 'region', 'description', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'e.g. Taj Mahal, Diwali, Bharatanatyam',
            }),
            'category': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'e.g. Monument, Festival, Art Form, Cuisine',
            }),
            'region': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'e.g. Uttar Pradesh, Kerala, All India',
            }),
            'description': forms.Textarea(attrs={
                'class': TEXTAREA_CLASSES,
                'placeholder': 'Write a detailed description — its history, significance, and why it matters...',
                'rows': 5,
            }),
            'latitude': forms.NumberInput(attrs={
                'class': INPUT_CLASSES_NO_ICON,
                'placeholder': 'e.g. 27.1751 (optional — used for map pin)',
                'step': 'any',
            }),
            'longitude': forms.NumberInput(attrs={
                'class': INPUT_CLASSES_NO_ICON,
                'placeholder': 'e.g. 78.0421 (optional — used for map pin)',
                'step': 'any',
            }),
        }

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise forms.ValidationError('Please provide a title for this heritage item.')

        # Case-insensitive duplicate check
        qs = HeritageItem.objects.filter(title__iexact=title)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            existing = qs.first()
            raise forms.ValidationError(
                f'"{title}" already exists in the Heritage Directory ({existing.category} in {existing.region}).'
            )
        return title
