PGDMP                     
    {            iam    15.4    15.4 /    -           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            .           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            /           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            0           1262    16404    iam    DATABASE     v   CREATE DATABASE iam WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
    DROP DATABASE iam;
                postgres    false            �            1259    16405    administrador    TABLE     �   CREATE TABLE public.administrador (
    id_administrador integer NOT NULL,
    correo character varying(100) NOT NULL,
    contrasena character varying(200) NOT NULL
);
 !   DROP TABLE public.administrador;
       public         heap    postgres    false            �            1259    16408 "   administrador_id_administrador_seq    SEQUENCE     �   CREATE SEQUENCE public.administrador_id_administrador_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE public.administrador_id_administrador_seq;
       public          postgres    false    214            1           0    0 "   administrador_id_administrador_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE public.administrador_id_administrador_seq OWNED BY public.administrador.id_administrador;
          public          postgres    false    215            �            1259    16472    diagnosticos    TABLE     �  CREATE TABLE public.diagnosticos (
    id_paciente integer NOT NULL,
    fecha date NOT NULL,
    probabilidad integer NOT NULL,
    dolor_pecho "char" NOT NULL,
    malestar "char" NOT NULL,
    mareo "char" NOT NULL,
    nauseas "char" NOT NULL,
    sudoracion "char" NOT NULL,
    extension_dolor "char" NOT NULL,
    lugar_extension character varying(100),
    id_diagnostico integer NOT NULL,
    azucar integer NOT NULL,
    presion integer NOT NULL,
    colesterol integer NOT NULL
);
     DROP TABLE public.diagnosticos;
       public         heap    postgres    false            �            1259    16477    diagnosticos_id_diagnostico_seq    SEQUENCE     �   CREATE SEQUENCE public.diagnosticos_id_diagnostico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.diagnosticos_id_diagnostico_seq;
       public          postgres    false    224            2           0    0    diagnosticos_id_diagnostico_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.diagnosticos_id_diagnostico_seq OWNED BY public.diagnosticos.id_diagnostico;
          public          postgres    false    225            �            1259    16415    estudios    TABLE     �   CREATE TABLE public.estudios (
    id_paciente integer NOT NULL,
    id_estudio integer NOT NULL,
    nombre_archivo character varying(100) NOT NULL,
    descripcion character varying(100) DEFAULT 'Nada'::character varying NOT NULL
);
    DROP TABLE public.estudios;
       public         heap    postgres    false            �            1259    16419    estudios_id_estudio_seq    SEQUENCE     �   CREATE SEQUENCE public.estudios_id_estudio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.estudios_id_estudio_seq;
       public          postgres    false    216            3           0    0    estudios_id_estudio_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.estudios_id_estudio_seq OWNED BY public.estudios.id_estudio;
          public          postgres    false    217            �            1259    16420 	   medicinas    TABLE     �   CREATE TABLE public.medicinas (
    id_medicina integer NOT NULL,
    id_paciente integer NOT NULL,
    dosis character varying(100) NOT NULL,
    nombre_medicina character varying(100) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_fin date
);
    DROP TABLE public.medicinas;
       public         heap    postgres    false            �            1259    16423    medicinas_id_medicina_seq    SEQUENCE     �   CREATE SEQUENCE public.medicinas_id_medicina_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.medicinas_id_medicina_seq;
       public          postgres    false    218            4           0    0    medicinas_id_medicina_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.medicinas_id_medicina_seq OWNED BY public.medicinas.id_medicina;
          public          postgres    false    219            �            1259    16424    medico    TABLE     !  CREATE TABLE public.medico (
    id_medico integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    cedula character varying(100) NOT NULL,
    correo character varying(100) NOT NULL,
    contrasena character varying(200) NOT NULL
);
    DROP TABLE public.medico;
       public         heap    postgres    false            �            1259    16429    medico_id_medico_seq    SEQUENCE     �   CREATE SEQUENCE public.medico_id_medico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.medico_id_medico_seq;
       public          postgres    false    220            5           0    0    medico_id_medico_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.medico_id_medico_seq OWNED BY public.medico.id_medico;
          public          postgres    false    221            �            1259    16430    paciente    TABLE     �   CREATE TABLE public.paciente (
    id_paciente integer NOT NULL,
    nombre character varying(100) NOT NULL,
    apellido character varying(100) NOT NULL,
    edad integer NOT NULL
);
    DROP TABLE public.paciente;
       public         heap    postgres    false            �            1259    16433    paciente_id_paciente_seq    SEQUENCE     �   CREATE SEQUENCE public.paciente_id_paciente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.paciente_id_paciente_seq;
       public          postgres    false    222            6           0    0    paciente_id_paciente_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.paciente_id_paciente_seq OWNED BY public.paciente.id_paciente;
          public          postgres    false    223            ~           2604    16434    administrador id_administrador    DEFAULT     �   ALTER TABLE ONLY public.administrador ALTER COLUMN id_administrador SET DEFAULT nextval('public.administrador_id_administrador_seq'::regclass);
 M   ALTER TABLE public.administrador ALTER COLUMN id_administrador DROP DEFAULT;
       public          postgres    false    215    214            �           2604    16478    diagnosticos id_diagnostico    DEFAULT     �   ALTER TABLE ONLY public.diagnosticos ALTER COLUMN id_diagnostico SET DEFAULT nextval('public.diagnosticos_id_diagnostico_seq'::regclass);
 J   ALTER TABLE public.diagnosticos ALTER COLUMN id_diagnostico DROP DEFAULT;
       public          postgres    false    225    224                       2604    16436    estudios id_estudio    DEFAULT     z   ALTER TABLE ONLY public.estudios ALTER COLUMN id_estudio SET DEFAULT nextval('public.estudios_id_estudio_seq'::regclass);
 B   ALTER TABLE public.estudios ALTER COLUMN id_estudio DROP DEFAULT;
       public          postgres    false    217    216            �           2604    16437    medicinas id_medicina    DEFAULT     ~   ALTER TABLE ONLY public.medicinas ALTER COLUMN id_medicina SET DEFAULT nextval('public.medicinas_id_medicina_seq'::regclass);
 D   ALTER TABLE public.medicinas ALTER COLUMN id_medicina DROP DEFAULT;
       public          postgres    false    219    218            �           2604    16438    medico id_medico    DEFAULT     t   ALTER TABLE ONLY public.medico ALTER COLUMN id_medico SET DEFAULT nextval('public.medico_id_medico_seq'::regclass);
 ?   ALTER TABLE public.medico ALTER COLUMN id_medico DROP DEFAULT;
       public          postgres    false    221    220            �           2604    16439    paciente id_paciente    DEFAULT     |   ALTER TABLE ONLY public.paciente ALTER COLUMN id_paciente SET DEFAULT nextval('public.paciente_id_paciente_seq'::regclass);
 C   ALTER TABLE public.paciente ALTER COLUMN id_paciente DROP DEFAULT;
       public          postgres    false    223    222                      0    16405    administrador 
   TABLE DATA           M   COPY public.administrador (id_administrador, correo, contrasena) FROM stdin;
    public          postgres    false    214   b8       )          0    16472    diagnosticos 
   TABLE DATA           �   COPY public.diagnosticos (id_paciente, fecha, probabilidad, dolor_pecho, malestar, mareo, nauseas, sudoracion, extension_dolor, lugar_extension, id_diagnostico, azucar, presion, colesterol) FROM stdin;
    public          postgres    false    224   D9       !          0    16415    estudios 
   TABLE DATA           X   COPY public.estudios (id_paciente, id_estudio, nombre_archivo, descripcion) FROM stdin;
    public          postgres    false    216   �9       #          0    16420 	   medicinas 
   TABLE DATA           n   COPY public.medicinas (id_medicina, id_paciente, dosis, nombre_medicina, fecha_inicio, fecha_fin) FROM stdin;
    public          postgres    false    218   :       %          0    16424    medico 
   TABLE DATA           Y   COPY public.medico (id_medico, nombre, apellido, cedula, correo, contrasena) FROM stdin;
    public          postgres    false    220   `:       '          0    16430    paciente 
   TABLE DATA           G   COPY public.paciente (id_paciente, nombre, apellido, edad) FROM stdin;
    public          postgres    false    222   �;       7           0    0 "   administrador_id_administrador_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.administrador_id_administrador_seq', 7, true);
          public          postgres    false    215            8           0    0    diagnosticos_id_diagnostico_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.diagnosticos_id_diagnostico_seq', 13, true);
          public          postgres    false    225            9           0    0    estudios_id_estudio_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.estudios_id_estudio_seq', 7, true);
          public          postgres    false    217            :           0    0    medicinas_id_medicina_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.medicinas_id_medicina_seq', 5, true);
          public          postgres    false    219            ;           0    0    medico_id_medico_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.medico_id_medico_seq', 7, true);
          public          postgres    false    221            <           0    0    paciente_id_paciente_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.paciente_id_paciente_seq', 11, true);
          public          postgres    false    223            �           2606    16441     administrador administrador_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.administrador
    ADD CONSTRAINT administrador_pkey PRIMARY KEY (id_administrador);
 J   ALTER TABLE ONLY public.administrador DROP CONSTRAINT administrador_pkey;
       public            postgres    false    214            �           2606    16445    estudios estudios_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.estudios
    ADD CONSTRAINT estudios_pkey PRIMARY KEY (id_estudio);
 @   ALTER TABLE ONLY public.estudios DROP CONSTRAINT estudios_pkey;
       public            postgres    false    216            �           2606    16447    medicinas medicinas_pkey 
   CONSTRAINT     _   ALTER TABLE ONLY public.medicinas
    ADD CONSTRAINT medicinas_pkey PRIMARY KEY (id_medicina);
 B   ALTER TABLE ONLY public.medicinas DROP CONSTRAINT medicinas_pkey;
       public            postgres    false    218            �           2606    16449    medico medico_pkey 
   CONSTRAINT     W   ALTER TABLE ONLY public.medico
    ADD CONSTRAINT medico_pkey PRIMARY KEY (id_medico);
 <   ALTER TABLE ONLY public.medico DROP CONSTRAINT medico_pkey;
       public            postgres    false    220            �           2606    16451    paciente paciente_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_pkey PRIMARY KEY (id_paciente);
 @   ALTER TABLE ONLY public.paciente DROP CONSTRAINT paciente_pkey;
       public            postgres    false    222            �           2606    16457    estudios id_paciente    FK CONSTRAINT     �   ALTER TABLE ONLY public.estudios
    ADD CONSTRAINT id_paciente FOREIGN KEY (id_paciente) REFERENCES public.paciente(id_paciente) ON DELETE CASCADE;
 >   ALTER TABLE ONLY public.estudios DROP CONSTRAINT id_paciente;
       public          postgres    false    216    222    3214            �           2606    16462    medicinas id_paciente    FK CONSTRAINT     �   ALTER TABLE ONLY public.medicinas
    ADD CONSTRAINT id_paciente FOREIGN KEY (id_paciente) REFERENCES public.paciente(id_paciente) ON DELETE CASCADE;
 ?   ALTER TABLE ONLY public.medicinas DROP CONSTRAINT id_paciente;
       public          postgres    false    222    3214    218               �   x����JAE���1�f���]LJ4>��̦'�Nӎ�%_o� ~��[P�{��*�<���a8�ݘ�����a��_RCW;�7���}�Yw�t���W˘�t�p�_�>O�?�����ue��������jJ�	�j�/ ��K�$dQ`/A�$*UX�R��L�efu�P8E��IRbG�uZ��I�EV�� �+�u�523������OU_�      )   U   x�3�4202�54�56�D��)��i�)i��F@E���@ld�e���̜�
Az����<�
K3S�R�9��ZL�ځ�+F��� ��      !   M   x�3�4�42�54�5202�7��74"���4Nל�䒢��Ģ�������DC.#NsNc��x�xSK�b���� �nF      #   J   x�3�4�4VH�QH�L�(*MMJT�MM�4202�54�54�2�t��L��M`��K�K��J�,�L��=... &�       %   =  x�}P�JA<�~E9�;���b4�@	�����nf㮣�D�_o��Ga��.��ڻӶ��6��8hà�w?���}ԩ�c/����u���������z]M���i�����.V�����>��i|�|�N�	=�};)�gW}���C��,nB�nR�7��6�m�ǫ�����@V=Z��"�V,��R�p�@D�T���jP�DQ�TeA��a�ml��td=��(���vѤ�M}^�:U�u�}]���*S�#b�R��RJh���I���\@�Ƙ%#��X3�6Y(ٛ5CL>�ZpK-v������,�~��x�      '   5   x�3��,NLJ��t�ϫJ�I��46��(*MMJ����M���44������ 8m}     